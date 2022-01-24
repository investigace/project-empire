from datetime import date, datetime
from re import sub
import requests
from pprint import pprint

import enlighten
from slugify import slugify

from ..convert_currency import convert_currency
from ..data import Subsidy, SubsidyPayment, SubsidySource

def fetch_subsidies(auth_token, legal_entities):
    subsidies_data = {
        'subsidies': [],
        'subsidies_payments': [],
        'subsidies_sources': []
    }

    progress_bar = enlighten.Counter(
        total=len(legal_entities), desc='Fetching subsidies from Hlidacstatu', unit='legal entities')

    for legal_entity in legal_entities:
        legal_entity_subsidies_data = fetch_subsidies_for_legal_entity(auth_token, legal_entity)

        subsidies_data['subsidies'] += legal_entity_subsidies_data['subsidies']
        subsidies_data['subsidies_payments'] += legal_entity_subsidies_data['subsidies_payments']
        subsidies_data['subsidies_sources'] += legal_entity_subsidies_data['subsidies_sources']

        progress_bar.update()

    return subsidies_data

def fetch_subsidies_for_legal_entity(auth_token, legal_entity):
    all_hs_subsidies = []
    page = 1

    while True:
        headers = {
            'Authorization': 'Token ' + auth_token,
            'Content-Type': 'application/json'
        }
        params = {
            'dotaz': 'ico:' + str(legal_entity.identification_number),
            'strana': page,
            'razeni': 2  # sort by date of signing, oldest first
        }

        r = requests.get('https://www.hlidacstatu.cz/api/v2/dotace/hledat', headers=headers, params=params)

        # pprint(r.request.url)
        # pprint(r.request.headers)
        # print(r.text)

        payload = r.json()

        if payload['total'] == 0:
            break

        if len(payload['results']) == 0:
            break

        all_hs_subsidies += payload['results']
        page += 1

    mapped_hs_subsidies = []
    remove_hs_ids = []

    for hs_subsidy in all_hs_subsidies:
        mapped_hs_subsidies.append({
            'hs_subsidy': hs_subsidy,
            'mapped_data': map_hlidacstatu_subsidy_to_empire_subsidy(legal_entity, hs_subsidy)
        })

        if hs_subsidy.get('duplicita'):
            # Hlidac statu returns the duplicate ID without being slugified
            duplicate_id = slugify(hs_subsidy['duplicita']).lower()

            if hs_subsidy['idDotace'].startswith('eufondy-') and duplicate_id.startswith('cedr-'):
                remove_hs_ids.append(duplicate_id)
            elif hs_subsidy['idDotace'].startswith('cedr-') and duplicate_id.startswith('cedr-'):
                remove_hs_ids.append(duplicate_id)
            elif hs_subsidy['idDotace'].startswith('deminimis-') and duplicate_id.startswith('eufondy-'):
                remove_hs_ids.append(hs_subsidy['idDotace'])
            elif hs_subsidy['idDotace'].startswith('dotinfo-') and duplicate_id.startswith('cedr-'):
                remove_hs_ids.append(hs_subsidy['idDotace'])
            elif hs_subsidy['idDotace'].startswith('dotinfo-') and duplicate_id.startswith('eufondy-'):
                remove_hs_ids.append(hs_subsidy['idDotace'])
            elif hs_subsidy['idDotace'].startswith('deminimis-') and duplicate_id.startswith('deminimis-'):
                remove_hs_ids.append(duplicate_id)
            elif hs_subsidy['idDotace'].startswith('deminimis-') and duplicate_id.startswith('cedr-'):
                remove_hs_ids.append(hs_subsidy['idDotace'])
            else:
                print(hs_subsidy['idDotace'])
                print(duplicate_id)
                raise Exception('Subsidy has duplicate, but there is no rule to remove it')

    # Remove duplicates
    mapped_hs_subsidies = list(filter(lambda mapped_hs_subsidy: mapped_hs_subsidy['hs_subsidy']['idDotace'] not in remove_hs_ids, mapped_hs_subsidies))

    subsidies_data = {
        'subsidies': [],
        'subsidies_payments': [],
        'subsidies_sources': []
    }

    for mapped_hs_subsidy in mapped_hs_subsidies:
        mapped_data = mapped_hs_subsidy['mapped_data']

        subsidies_data['subsidies'] += mapped_data['subsidies']
        subsidies_data['subsidies_payments'] += mapped_data['subsidies_payments']
        subsidies_data['subsidies_sources'] += mapped_data['subsidies_sources']

    return subsidies_data

def map_hlidacstatu_subsidy_to_empire_subsidy(legal_entity, hs_subsidy):
    # print('')
    # print('================================================================================')
    # pprint(hs_subsidy)
    # print('-----------------------------------------------------------------')

    database_identifier = hs_subsidy['idDotace']

    if database_identifier.startswith('cedr-'):
        database_identifier = database_identifier.replace('cedr-', 'CEDR-', 1)
    elif database_identifier.startswith('szif-'):
        database_identifier = database_identifier.replace('szif-', 'SZIF-', 1)
    elif database_identifier.startswith('dotinfo-'):
        database_identifier = database_identifier.replace('dotinfo-', 'DOTINFO-', 1)
    elif database_identifier.startswith('eufondy-'):
        database_identifier = database_identifier.replace('eufondy-', 'EUFONDY-', 1)
    elif database_identifier.startswith('czechinvest-'):
        database_identifier = database_identifier.replace('czechinvest-', 'CZECHINVEST-', 1)
    elif database_identifier.startswith('deminimis-'):
        database_identifier = database_identifier.replace('deminimis-', 'DEMINIMIS-', 1)
    else:
        raise Exception('Unknown id prefix ' + database_identifier)

    project_name = database_identifier
    if 'nazevProjektu' in hs_subsidy:
        project_name = hs_subsidy['nazevProjektu']

    project_code = None
    if 'kodProjektu' in hs_subsidy:
        project_code = hs_subsidy['kodProjektu']

    programme_name = None
    if 'program' in hs_subsidy and hs_subsidy['program'] and 'nazev' in hs_subsidy['program']:
        programme_name = hs_subsidy['program']['nazev']

    programme_code = None
    if 'program' in hs_subsidy and hs_subsidy['program'] and 'kod' in hs_subsidy['program']:
        programme_code = hs_subsidy['program']['kod']

    signed_on = None
    if hs_subsidy.get('datumPodpisu'):
        datetime_obj = None

        try:
            datetime_obj = datetime.strptime(hs_subsidy['datumPodpisu'], '%Y-%m-%dT00:00:00')
        except ValueError:
            pass

        try:
            datetime_obj = datetime.strptime(hs_subsidy['datumPodpisu'], '%Y-%m-%dT00:00:00Z')
        except ValueError:
            pass

        if datetime_obj:
            signed_on = datetime_obj.date()

    subsidy_payments_data = []
    for hs_rozhodnuti in hs_subsidy['rozhodnuti']:
        provider = hs_rozhodnuti['poskytovatel']
        if not provider and 'zdrojFinanci' in hs_rozhodnuti:
            provider = hs_rozhodnuti['zdrojFinanci']

        requested_amount = None
        if 'castkaPozadovana' in hs_rozhodnuti:
            requested_amount = hs_rozhodnuti['castkaPozadovana']

        decided_amount = None
        if 'castkaRozhodnuta' in hs_rozhodnuti:
            decided_amount = hs_rozhodnuti['castkaRozhodnuta']

        drawed_amount = None
        if 'cerpanoCelkem' in hs_rozhodnuti:
            drawed_amount = hs_rozhodnuti['cerpanoCelkem']

        amount_in_original_currency = None
        if drawed_amount:
            amount_in_original_currency = float(drawed_amount)
        elif decided_amount:
            amount_in_original_currency = float(decided_amount)
        elif requested_amount:
            amount_in_original_currency = float(requested_amount)

        payment_year = None
        if hs_rozhodnuti.get('rok'):
            payment_year = str(hs_rozhodnuti['rok'])

        conversion_year = payment_year
        if not conversion_year and signed_on:
            conversion_year = signed_on.year
        elif not conversion_year and project_name and project_name.startswith('CZ.1.02/'):
            # dotinfo subsidies
            conversion_year = '2007'            

        (amount_in_eur, conversion_note) = convert_currency(amount_in_original_currency, 'CZK', 'EUR', conversion_year)

        payment_notes = ''
        if requested_amount:
            payment_notes += 'Částka požadovaná: ' + str(requested_amount) + "\n"
        if decided_amount:
            payment_notes += 'Částka rozhodnutá: ' + str(decided_amount) + "\n"
        if drawed_amount:
            payment_notes += 'Částka čerpaná: ' + str(drawed_amount) + "\n"
        if conversion_note:
            payment_notes += conversion_note + "\n"
        
        subsidy_payments_data.append({
            'provider': provider,
            'year': payment_year,
            'original_currency': 'CZK',
            'amount_in_original_currency': amount_in_original_currency,
            'amount_in_eur': amount_in_eur,
            'notes': payment_notes.strip()
        })

    year = None
    if len(subsidy_payments_data) > 0 and subsidy_payments_data[0]['year']:
        year = subsidy_payments_data[0]['year']
    elif signed_on:
        year = signed_on.year
    elif project_name.startswith('CZ.1.02/'):
        # dotinfo subsidies
        year = '2007-2013'

    notes = ''
    if signed_on:
        notes += 'Datum podpisu: ' + str(signed_on) + "\n\n"

    subsidy = Subsidy(**{
        'database_identifier': database_identifier,
        'receiving_legal_entity': legal_entity,
        'project_name': project_name,
        'project_code': project_code,
        'programme_name': programme_name,
        'programme_code': programme_code,
        'year': year,
        'notes': notes.strip()
    })

    subsidy_payments = []
    for subsidy_payment_data in subsidy_payments_data:
        subsidy_payments.append(SubsidyPayment(subsidy=subsidy, **subsidy_payment_data))

    subsidy_sources = [SubsidySource(**{
        'subsidy': subsidy,
        'summary': f"Záznam dotace {hs_subsidy['idDotace']} v databázi Hlídač státu",
        'information_gained_from_source': '',
        'last_checked_date': str(datetime.now().date()),
        'url': f"https://www.hlidacstatu.cz/Dotace/Detail/{hs_subsidy['idDotace']}"
    })]

    
    # pprint(subsidy)
    # pprint(subsidy_payments)
    # pprint(subsidy_sources)

    return {
        'subsidies': [subsidy],
        'subsidies_payments': subsidy_payments,
        'subsidies_sources': subsidy_sources
    }
