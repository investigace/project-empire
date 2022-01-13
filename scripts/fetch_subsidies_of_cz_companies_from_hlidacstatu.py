#!/usr/bin/env python3

import argparse
from os import getenv
from os.path import join, dirname, abspath
from pprint import pprint
import sys

import openpyxl
from prompt_toolkit.shortcuts import confirm, prompt

import empire

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch subsidies of CZ companies in Empire database from Hlidacstatu.cz')
    parser.add_argument(
        'database_excel',
        metavar="DATABASE_EXCEL",
        help='Path to the Excel spreadsheet file with Empire database'
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # TODO
    hlidacstatu_auth_token = '8af24927cea0451787d6fd4db34e6288'
    # hlidacstatu_auth_token = prompt(
    #     message=f'Hlidacstatu AUTH token: ',
    #     is_password=True
    # )

    out_excel_path = abspath(join(dirname(__file__), 'subsidies_of_cz_companies_from_hlidacstatu.xlsx'))

    # Load data

    empire_data = empire.load_excel(args.database_excel)

    print(f"Loaded Empire database: {len(empire_data['legal_entities'])} legal entities, {len(empire_data['people'])} people, {len(empire_data['subsidies'])} subsidies")

    # Check connection to Hlidacstatu

    hlidacstatu = empire.Hlidacstatu(hlidacstatu_auth_token)

    print('Connected to Hlidacstatu with the provided AUTH token')

    # Filter out CZ legal entites with identifier

    cz_legal_entites = list(filter(lambda c: c.country == 'CZ' and c.identification_number is not None, empire_data['legal_entities']))

    print(f"Will fetch subsidies for {len(cz_legal_entites)} legal entities from CZ country which have identification number filled")

    # Check if continue

    answer = confirm("Do you want to continue?")
    if answer != True:
        print('Ok, exiting')
        exit(0)

    # Fetch and save to Excel file

    fetched_subsidies = hlidacstatu.fetch_subsidies(cz_legal_entites)

    wb = openpyxl.Workbook()
    
    default_sheet = wb.active
    subsidies_sheet = wb.create_sheet(title="3. Subsidies", index=0)
    subsidies_payments_sheet = wb.create_sheet(title="3.1. Subsidies payments", index=1)
    subsidies_sources_sheet = wb.create_sheet(title="3.2. Subsidies sources", index=2)
    wb.remove(default_sheet)

    # TODO: 

    wb.save(out_excel_path)

    print(f'Subsidies fetched and saved to Excel file {out_excel_path}')
