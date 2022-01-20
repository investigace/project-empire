from pprint import pprint

import iso3166

from .countries import get_countries_in_other_group
from .page_templates import render_page_template


def prepare_summary_changes(mediawiki, empire_data):
    changes = {
        'pages': {
            'create': [],
            'update': [],
            'delete': []
        }
    }

    page = prepare_summary_table_page(empire_data, mediawiki.lang)
    mediawiki_page = mediawiki.site.pages[page['name']]

    if mediawiki_page.exists:
        mediawiki_page_content = mediawiki_page.text()

        if mediawiki_page_content != page['content']:
            changes['pages']['update'].append({
                'name': page['name'],
                'content_current': mediawiki_page_content,
                'content_change': page['content']
            })
    else:
        changes['pages']['create'].append({
            'name': page['name'],
            'content_change': page['content']
        })

    return changes


def prepare_summary_table_page(empire_data, lang):
    countries_dict = {}

    if 'legal_entities' in empire_data:
        for legal_entity in empire_data['legal_entities']:
            if legal_entity.country not in countries_dict:
                countries_dict[legal_entity.country] = {
                    'legal_entities_count': 0,
                    'people_count': 0,
                    'subsidies_count': 0,
                    'subsidies_sum': 0.0
                }

            countries_dict[legal_entity.country]['legal_entities_count'] += 1

    if 'people' in empire_data:
        for person in empire_data['people']:
            if person.nationality not in countries_dict:
                countries_dict[person.nationality] = {
                    'legal_entities_count': 0,
                    'people_count': 0,
                    'subsidies_count': 0,
                    'subsidies_sum': 0.0
                }

            countries_dict[person.nationality]['people_count'] += 1

    for subsidy in empire_data.get('subsidies', []):
        if subsidy.receiving_legal_entity.country not in countries_dict:
            countries_dict[subsidy.receiving_legal_entity.country] = {
                'legal_entities_count': 0,
                'people_count': 0,
                'subsidies_count': 0,
                'subsidies_sum': 0.0
            }

        payments_sum = 0.0
        for payment in (p for p in empire_data['subsidies_payments'] if p.subsidy == subsidy):
            if payment.amount_in_eur:
                payments_sum += payment.amount_in_eur

        countries_dict[subsidy.receiving_legal_entity.country]['subsidies_count'] += 1
        countries_dict[subsidy.receiving_legal_entity.country]['subsidies_sum'] += payments_sum

    countries_in_other_group = get_countries_in_other_group(empire_data)

    countries = []
    other_countries_item = {
        'name': 'Other countries',
        'legal_entities_count': 0,
        'people_count': 0,
        'subsidies_count': 0,
        'subsidies_sum': 0.0
    }

    for country_code, country_data in countries_dict.items():
        if country_code in countries_in_other_group:
            other_countries_item['legal_entities_count'] += country_data['legal_entities_count']
            other_countries_item['people_count'] += country_data['people_count']
            other_countries_item['subsidies_count'] += country_data['subsidies_count']
            other_countries_item['subsidies_sum'] += country_data['subsidies_sum']
        else:
            countries.append({
                'code': country_code,
                'name': iso3166.countries.get(country_code).name,
                **country_data
            })

    countries = sorted(countries, key=lambda country: country['name'])

    if other_countries_item['legal_entities_count'] > 0 or other_countries_item['people_count'] > 0 or other_countries_item['subsidies_count'] > 0:
        countries.append(other_countries_item)

    totals = {
        'legal_entities_count': 0,
        'people_count': 0,
        'subsidies_count': 0,
        'subsidies_sum': 0.0
    }
    for country in countries:
        totals['legal_entities_count'] += country['legal_entities_count']
        totals['people_count'] += country['people_count']
        totals['subsidies_count'] += country['subsidies_count']
        totals['subsidies_sum'] += country['subsidies_sum']

    return render_page_template(lang, 'summary_table_template.mako', {'countries': countries, 'totals': totals})
