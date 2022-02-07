import locale
import json
from os.path import join, dirname, isfile
from pprint import pprint
import re
from time import sleep
import requests
import tempfile

import enlighten
import iso3166
import xmltodict

from ..data import OtherRelationship, Owner


ARES_API_TIMEOUT = 10


def fetch_relationships(legal_entities, cache_ares_xmls=False):
    locale.setlocale(locale.LC_ALL, 'cs_CZ')
    temp_dir_path = tempfile.gettempdir()

    if cache_ares_xmls:
        print(f'Caching ARES xmls in temp dir {temp_dir_path}')

    progress_bar = enlighten.Counter(
        total=len(legal_entities), desc='Fetching xmls from ARES', unit='xmls')
    progress_bar.refresh()

    ares_xmls = {}

    for legal_entity in legal_entities:
        cache_path = join(
            temp_dir_path, f'{legal_entity.identification_number}.xml')
        ares_xml = None

        if cache_ares_xmls and isfile(cache_path):
            with open(cache_path, 'r') as cache_file:
                ares_xml = cache_file.read()

        else:
            ares_url = f"https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_vr.cgi?ico={legal_entity.identification_number}&rozsah=1"
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }

            try:
                response = requests.get(ares_url, headers=headers, timeout=ARES_API_TIMEOUT)
            except requests.exceptions.ReadTimeout:
                print(
                    f"Error: Fetching xml timed out after {ARES_API_TIMEOUT}s, ARES url: {ares_url}")
                exit(1)

            response.raise_for_status()

            # Force use utf-8 for decoding the payload, because otherwise the content
            # will be decoded wrongly using iso-8859-1
            response.encoding = 'utf-8'

            ares_xml = response.text

            if cache_ares_xmls:
                with open(cache_path, 'w') as cache_file:
                    cache_file.write(ares_xml)

        ares_xmls[legal_entity.database_identifier] = ares_xml

        progress_bar.update()

    fetched_empire_data = {
        'legal_entities_owners': [],
        'legal_entities_other_relationships': []
    }

    progress_bar = enlighten.Counter(
        total=len(legal_entities), desc='Parsing xmls from ARES', unit='xmls')
    progress_bar.refresh()

    for legal_entity in legal_entities:
        ares_xml_dict = xmltodict.parse(ares_xmls[legal_entity.database_identifier])
        
        owners = parse_owners(ares_xml_dict, legal_entity)
        other_relationships = parse_other_relationships(ares_xml_dict, legal_entity)

        fetched_empire_data['legal_entities_owners'] += owners
        fetched_empire_data['legal_entities_other_relationships'] += other_relationships

        progress_bar.update()

    return fetched_empire_data


def parse_owners(ares_xml_dict, legal_entity):
    company_data = ares_xml_dict['are:Ares_odpovedi']['are:Odpoved']['are:Vypis_VR']

    if isinstance(company_data, list):
        company_data = company_data[0]

    owners = []

    # SHARE OWNERS

    spolecnici_data = company_data.get('are:Spolecnici')
    spolecnik_data_list = spolecnici_data.get('are:Spolecnik', []) if spolecnici_data else []

    if not isinstance(spolecnik_data_list, list):
        spolecnik_data_list = [spolecnik_data_list]

    for spolecnik_data in spolecnik_data_list:
        owner_data = {
            'owned_legal_entity': legal_entity
        }

        if 'are:fosoba' in spolecnik_data:
            owner_data = {
                **owner_data,
                'owner_type': 'Person',
                **parse_fosoba(spolecnik_data['are:fosoba'], 'owner_')
            }

        if 'are:posoba' in spolecnik_data:
            owner_data = {
                **owner_data,
                'owner_type': 'Legal entity',
                **parse_posoba(spolecnik_data['are:posoba'], 'owner_')
            }

        podil_data_list = spolecnik_data.get('are:Podil', [])

        # Mostly there is only one share so we just make sure it is list
        if not isinstance(podil_data_list, list):
            podil_data_list = [podil_data_list]

        for podil_data in podil_data_list:
            
            # PERCENTAGE

            percentage = None
            
            velikost_podilu_data = podil_data.get('are:velikostPodilu')
            if velikost_podilu_data:
                if velikost_podilu_data['are:typ'] == 'PROCENTA':
                    percentage = parse_percents(velikost_podilu_data['are:value'])
                elif velikost_podilu_data['are:typ'] == 'TEXT':
                    matches = re.search(r'(\d+)', velikost_podilu_data['are:value'])
                    percentage = float(matches[0]) if matches else velikost_podilu_data['are:value']

            owner_data['owned_percentage'] = percentage

            # DETAILS

            details = []

            vklad_data = podil_data.get('are:vklad')
            if vklad_data and vklad_data['are:typ'] == 'KORUNY':
                details.append(f"Vklad: {format_currency(parse_currency(vklad_data['are:value']))}.")

            splaceni_data = podil_data.get('are:splaceni')
            if splaceni_data:
                if splaceni_data['are:typ'] == 'KORUNY':
                    details.append(f"Splaceno: {format_currency(parse_currency(splaceni_data['are:value']))}.")
                elif splaceni_data['are:typ'] == 'PROCENTA':
                    details.append(f"Splaceno: {parse_percents(splaceni_data['are:value']):n} %.")

            owner_data['ownership_details'] = ' '.join(details)

            # SINCE & UNTIL DATES

            owner_data['owned_since_date'] = podil_data.get('@dza')
            owner_data['owned_until_date'] = podil_data.get('@dvy')

            owners.append(Owner(**owner_data))

    # STOCK OWNERS

    jinyorgan_data_list = company_data.get('are:JinyOrgan', [])

    if not isinstance(jinyorgan_data_list, list):
        jinyorgan_data_list = [jinyorgan_data_list]

    for jinyorgan_data in jinyorgan_data_list:
        if jinyorgan_data['are:Nazev'] in ['Jediný akcionář', 'Akcionáři']:
            clen_data_list = jinyorgan_data.get('are:Clen', [])

            if not isinstance(clen_data_list, list):
                clen_data_list = [clen_data_list]

            for clen_data in clen_data_list:
                owner_data = {
                    'owned_legal_entity': legal_entity,
                    'owned_percentage': None,
                    'ownership_details': 'Akcionář',
                    'owned_since_date': clen_data.get('@dza'),
                    'owned_until_date': clen_data.get('@dvy')
                }

                if 'are:fosoba' in clen_data:
                    owner_data = {
                        **owner_data,
                        'owner_type': 'Person',
                        **parse_fosoba(clen_data['are:fosoba'], 'owner_')
                    }

                if 'are:posoba' in clen_data:
                    owner_data = {
                        **owner_data,
                        'owner_type': 'Legal entity',
                        **parse_posoba(clen_data['are:posoba'], 'owner_')
                    }

                owners.append(Owner(**owner_data))

    return owners


def parse_other_relationships(ares_xml_dict, legal_entity):
    company_data = ares_xml_dict['are:Ares_odpovedi']['are:Odpoved']['are:Vypis_VR']

    if isinstance(company_data, list):
        company_data = company_data[0]

    other_relationships = []

    # STATUTORY AUTHORITY

    statutarniorgan_data_list = company_data.get('are:StatutarniOrgan', [])

    if not isinstance(statutarniorgan_data_list, list):
        statutarniorgan_data_list = [statutarniorgan_data_list]

    for statutarniorgan_data in statutarniorgan_data_list:
        clen_data_list = statutarniorgan_data.get('are:Clen', [])

        if not isinstance(clen_data_list, list):
            clen_data_list = [clen_data_list]

        for clen_data in clen_data_list:
            relationship_data = {
                'legal_entity': legal_entity
            }

            if 'are:fosoba' in clen_data:
                relationship_data = {
                    **relationship_data,
                    'related_type': 'Person',
                    **parse_fosoba(clen_data['are:fosoba'], 'related_')
                }

            if 'are:posoba' in clen_data:
                relationship_data = {
                    **relationship_data,
                    'related_type': 'Legal entity',
                    **parse_posoba(clen_data['are:posoba'], 'related_')
                }

            # DETAILS

            details = statutarniorgan_data['are:Nazev'] + '.'

            funkce_data = clen_data.get('are:funkce')
            if funkce_data and 'are:nazev' in funkce_data:
                details += f" Funkce: {funkce_data['are:nazev']}."

            relationship_data['relationship_details'] = details

            # SINCE DATE

            since_date = clen_data.get('@dza')

            clenstvi_data = clen_data.get('are:clenstvi')
            if clenstvi_data and 'are:vznikClenstvi' in clenstvi_data:
                since_date = clenstvi_data['are:vznikClenstvi']

            funkce_data = clen_data.get('are:funkce')
            if funkce_data and 'are:vznikFunkce' in funkce_data:
                since_date = funkce_data['are:vznikFunkce']

            relationship_data['related_since_date'] = since_date

            # UNTIL DATE

            until_date = clen_data.get('@dvy')

            clenstvi_data = clen_data.get('are:clenstvi')
            if clenstvi_data and 'are:zanikClenstvi' in clenstvi_data:
                until_date = clenstvi_data['are:zanikClenstvi']

            funkce_data = clen_data.get('are:funkce')
            if funkce_data and 'are:zanikFunkce' in funkce_data:
                until_date = funkce_data['are:zanikFunkce']

            relationship_data['related_until_date'] = until_date
            
            other_relationships.append(OtherRelationship(**relationship_data))

    # OTHER RELATIONSHIPS

    jinyorgan_data_list = company_data.get('are:JinyOrgan', [])

    if not isinstance(jinyorgan_data_list, list):
        jinyorgan_data_list = [jinyorgan_data_list]

    for jinyorgan_data in jinyorgan_data_list:
        if jinyorgan_data['are:Nazev'] not in ['Jediný akcionář', 'Akcionáři']:
            clen_data_list = jinyorgan_data.get('are:Clen', [])

            if not isinstance(clen_data_list, list):
                clen_data_list = [clen_data_list]

            for clen_data in clen_data_list:
                relationship_data = {
                    'legal_entity': legal_entity
                }

                if 'are:fosoba' in clen_data:
                    relationship_data = {
                        **relationship_data,
                        'related_type': 'Person',
                        **parse_fosoba(clen_data['are:fosoba'], 'related_')
                    }

                if 'are:posoba' in clen_data:
                    relationship_data = {
                        **relationship_data,
                        'related_type': 'Legal entity',
                        **parse_posoba(clen_data['are:posoba'], 'related_')
                    }

                # DETAILS

                details = jinyorgan_data['are:Nazev'] + '.'

                funkce_data = clen_data.get('are:funkce')
                if funkce_data and 'are:nazev' in funkce_data:
                    details += f" Funkce: {funkce_data['are:nazev']}."

                relationship_data['relationship_details'] = details

                # SINCE DATE

                since_date = clen_data.get('@dza')

                funkce_data = clen_data.get('are:funkce')
                if funkce_data and 'are:vznikFunkce' in funkce_data:
                    since_date = funkce_data['are:vznikFunkce']

                relationship_data['related_since_date'] = since_date

                # UNTIL DATE

                until_date = clen_data.get('@dvy')

                funkce_data = clen_data.get('are:funkce')
                if funkce_data and 'are:zanikFunkce' in funkce_data:
                    until_date = funkce_data['are:zanikFunkce']

                relationship_data['related_until_date'] = until_date

                other_relationships.append(OtherRelationship(**relationship_data))

    return other_relationships


def parse_fosoba(fosoba_data, prefix):
    full_name = f"{fosoba_data.get('are:jmeno', '').lower().capitalize()} {fosoba_data.get('are:prijmeni', '').lower().capitalize()}"

    # If 'jmeno' is missing, we dont want the space before 'prijmeni'
    full_name = full_name.strip()

    address_data = fosoba_data.get('are:adresa')
    if not address_data:
        address_data = fosoba_data.get('are:bydliste')

    return {
        f'{prefix}name': full_name,
        f'{prefix}person_date_of_birth': fosoba_data.get('are:datumNarozeni'),
        f'{prefix}address': parse_address(address_data),
        f'{prefix}country': parse_country(address_data)
    }

def parse_posoba(posoba_data, prefix):
    return {
        f'{prefix}name': posoba_data['are:ObchodniFirma']['dtt:value'],
        f'{prefix}legal_entity_identification_number': posoba_data['are:Ico']['dtt:value'] if 'are:Ico' in posoba_data else None,
        f'{prefix}address': parse_address(posoba_data['are:adresa']),
        f'{prefix}country': parse_country(posoba_data['are:adresa'])
    }

def parse_address(address_data):
    address_parts = []

    text = address_data.get('dtt:TextAdresa')
    if text:
        address_parts.append(text.strip())

    street = address_data.get('dtt:NazevUvp')
    street_no_txt = address_data.get('dtt:CisloTxt')
    street_no_house = address_data.get('dtt:CisloDomu')
    street_no_house_type = address_data.get('dtt:TypCisDom')
    street_no_orientation = address_data.get('dtt:CisloOr')                
    if street:
        part = street

        if street_no_txt:
            part += f' {street_no_txt}'

        if street_no_house and street_no_house_type and street_no_house_type == '1':
            part += f' {street_no_house}'

            if street_no_orientation:
                part += f'/{street_no_orientation}'

        address_parts.append(part.strip())

    city_part = address_data.get('dtt:NazevCastob')
    if city_part:
        address_parts.append(city_part.strip())

    city = address_data.get('dtt:NazevObce', '')
    zip = address_data.get('dtt:Psc', '')
    if city != '' or zip != '':
        address_parts.append(f'{zip} {city}'.strip())

    region = address_data.get('dtt:NazevOkresu')
    if region:
        address_parts.append(region.strip())

    country = address_data.get('dtt:NazevStatu')
    if country:
        address_parts.append(country.strip())

    return ', '.join(address_parts)

def parse_country(address_data):
    numeric_code = address_data.get('dtt:KodStatu')
    if not numeric_code:
        return None

    iso3166_country = iso3166.countries_by_numeric.get(numeric_code)
    if not iso3166_country:
        return None

    return iso3166_country.alpha2

def parse_currency(value):
    return float(value.replace(';', '.').replace(',', '.'))

def format_currency(value):
    return locale.format_string('%.0f', value, True) + ' Kč'

def parse_percents(value):
    return float(value.replace(';', '.').replace(',', '.'))

