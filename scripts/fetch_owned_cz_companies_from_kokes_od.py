#!/usr/bin/env python3

import argparse
import json
from os import getenv
from os.path import join, dirname, abspath
from pprint import pprint
import sys

import openpyxl
import psycopg2
from prompt_toolkit.shortcuts import confirm, prompt

import empire


def parse_address_json(address_json):
    address = ''

    if 'text' in address_json:
        address += address_json['text']

    if 'ulice' in address_json:
        address += address_json['ulice']
    if 'ulice' not in address_json and 'obec' in address_json and ('cisloTxt' in address_json or 'cisloPop' in address_json or 'cisloOr' in address_json):
        address += address_json['obec']

    if 'cisloTxt' in address_json:
        address += ' ' + address_json['cisloTxt']
    if 'cisloPop' in address_json:
        address += ' ' + address_json['cisloPop']
    if 'cisloOr' in address_json:
        address += '/' + address_json['cisloOr']

    if ('obec' in address_json or 'psc' in address_json) and address != '':
        address += ', '

    if 'obec' in address_json and 'psc' in address_json:
        address += address_json['psc'] + ' ' + address_json['obec']
    if 'obec' in address_json and 'psc' not in address_json:
        address += address_json['obec']
    if 'obec' not in address_json and 'psc' in address_json:
        address += address_json['psc']

    return address


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Fetch owned companies of CZ companies in Empire database from kokes/od')
    parser.add_argument(
        'database_excel',
        metavar="DATABASE_EXCEL",
        help='Path to the Excel spreadsheet file with Empire database'
    )
    parser.add_argument(
        'kokesod_postgres_connstring',
        metavar="KOKESOD_POSTGRES_CONNSTRING",
        help='Connection string to the PostgreSQL database with kokes/od ares'
    )
    parser.add_argument(
        '-y',
        '--yes',
        help='Do not ask whether to continue and just continue with fetching',
        action='store_true'
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Load data

    print('Loading Empire database...')

    empire_data = empire.load_excel(args.database_excel)

    print(
        f"Loaded Empire database: {len(empire_data['legal_entities'])} legal entities, {len(empire_data['people'])} people, {len(empire_data['subsidies'])} subsidies")

    # Connect to db

    print(f'Connecting to kokes/od database, schema aress...')

    conn = psycopg2.connect(
        args.kokesod_postgres_connstring, options='-c search_path=ares')

    print(f'Connected!')

    # Filter out CZ legal entites with identifier

    cz_legal_entites = list(filter(
        lambda c: c.country == 'CZ' and c.identification_number is not None, empire_data['legal_entities']))

    print(
        f"Will fetch owned companies for {len(cz_legal_entites)} legal entities from CZ country which have identification number filled")

    # Check if continue

    if not args.yes:
        answer = confirm("Do you want to continue?")
        if answer != True:
            print('Ok, exiting')
            exit(0)

    # Fetch!

    new_legal_entities = []

    with conn.cursor() as cur:
        for owner_legal_entity in cz_legal_entites:

            cur.execute("""
                SELECT
                    "ico",
                    "nazev_organu"
                FROM posoby
                WHERE "ico_organ" = %(identifier)s
                """,
                        {'identifier': int(owner_legal_entity.identification_number)})

            posoby_records = list(cur.fetchall())

            # pprint(posoby_records)
            # exit(1)

            for posoby_record in posoby_records:
                (
                    ico,
                    nazev_organu
                ) = posoby_record

                if nazev_organu not in ['Akcionáři', 'Jediný akcionář', 'Společníci']:
                    print(
                        f'Skipping posoby record for owner {owner_legal_entity.name}, because nazev_organu={nazev_organu}')
                    continue

                owned_legal_entity = next((le for le in empire_data['legal_entities'] if le.country == 'CZ' and int(
                    le.identification_number) == ico), None)

                if owned_legal_entity:
                    print(
                        f'Skipping posoby record for owner {owner_legal_entity.name}, because owned company {owned_legal_entity.name} is already in empire db')
                    continue

                cur.execute("""
                    SELECT
                        "obchodni_firma",
                        "datum_zapisu",
                        "datum_vymazu",
                        "sidlo"
                    FROM firmy
                    WHERE "ico" = %(ico)s
                    """,
                            {'ico': ico})

                firmy_record = list(cur.fetchall())[0]
                (
                    obchodni_firma,
                    datum_zapisu,
                    datum_vymazu,
                    sidlo
                ) = firmy_record

                # pprint(firmy_record)
                address = parse_address_json(sidlo)
                # pprint(address)

                found_new_legal_entity = next((le for le in new_legal_entities if le.identification_number == ico), None)
                if found_new_legal_entity:
                    continue

                new_legal_entities.append(empire.LegalEntity(**{
                    'database_identifier': obchodni_firma,
                    'legal_entity_type': 'Company',
                    'name': obchodni_firma,
                    'country': 'CZ',
                    'address': address,
                    'identification_number': ico,
                    'foundation_date': datum_zapisu,
                    'dissolution_date': datum_vymazu,
                    'other_notes': f'Zdroj: ARES https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_or.cgi?ico={ico}&rozsah=1'
                }))

    # pprint(new_legal_entities)
    # exit(1)

    wb = openpyxl.Workbook()
    
    le_sheet = wb.active
    le_sheet.title = '1. Legal entities'
    le_sheet.append([
        'Database identifier',
        'Legal entity type',
        'Name',
        'Country',
        'Identification number',
        'Address',
        'Foundation date',
        'Dissolution date',
        'Other notes'
    ])
    for legal_entity in new_legal_entities:
        le_sheet.append([
            legal_entity.database_identifier,
            legal_entity.legal_entity_type,
            legal_entity.name,
            legal_entity.country,
            legal_entity.identification_number,
            legal_entity.address,
            legal_entity.foundation_date,
            legal_entity.dissolution_date,
            legal_entity.other_notes
        ])
    
    out_excel_path = abspath(join(dirname(__file__), 'legal_entities.xlsx'))
    wb.save(out_excel_path)

    print(f'Legal entities fetched and saved to Excel file {out_excel_path}')
