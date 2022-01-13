import requests
from pprint import pprint

def fetch_subsidies(auth_token, legal_entities):
    subsidies_data = {
        'subsidies': [],
        'subsidies_payments': [],
        'subsidies_sources': []
    }

    # TODO
    legal_entities = list(filter(lambda le: le.database_identifier == 'Synthesia, a.s.', legal_entities))

    for legal_entity in legal_entities:
        legal_entity_subsidies_data = fetch_subsidies_for_legal_entity(auth_token, legal_entity)

        subsidies_data['subsidies'] += legal_entity_subsidies_data['subsidies']
        subsidies_data['subsidies_payments'] += legal_entity_subsidies_data['subsidies_payments']
        subsidies_data['subsidies_sources'] += legal_entity_subsidies_data['subsidies_sources']

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
            'dotaz': 'ico:' + legal_entity.identification_number,
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

    pprint(len(all_hs_subsidies))
    exit(1)

    return {
        'subsidies': [],
        'subsidies_payments': [],
        'subsidies_sources': []
    }
