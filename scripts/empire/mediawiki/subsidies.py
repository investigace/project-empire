from pprint import pprint

import enlighten
from iso3166 import countries

from .countries import get_countries_in_other_group
from .page_templates import render_page_template, prepare_template, render_prepared_template


def prepare_subsidies_changes(mediawiki, empire_data):
    changes = {
        'pages': {
            'create': [],
            'update': [],
            'delete': []
        }
    }

    # Subsidy pages

    keep_page_names = []

    progress_bar = enlighten.Counter(
            total=len(empire_data.get('subsidies', [])), desc='Preparing subsidy pages', unit='pages')

    subsidy_template = prepare_template(mediawiki.lang, 'subsidy.mako')
    
    payments_by_subsidy = {}
    for payment in empire_data.get('subsidies_payments', []):
        if not payment.subsidy.database_identifier in payments_by_subsidy:
            payments_by_subsidy[payment.subsidy.database_identifier] = []
        payments_by_subsidy[payment.subsidy.database_identifier].append(payment)

    sources_by_subsidy = {}
    for source in empire_data.get('subsidies_sources', []):
        if not source.subsidy.database_identifier in sources_by_subsidy:
            sources_by_subsidy[source.subsidy.database_identifier] = []
        sources_by_subsidy[source.subsidy.database_identifier].append(source)

    for subsidy in empire_data.get('subsidies', []):
        page = prepare_subsidy_page(subsidy, payments_by_subsidy, sources_by_subsidy, mediawiki.lang, subsidy_template)
        page_name = page['name']
        page_content = page['content']

        mediawiki_page = mediawiki.site.pages[page_name]

        if mediawiki_page.exists:
            mediawiki_page_content = mediawiki_page.text()

            if mediawiki_page_content != page_content:
                changes['pages']['update'].append({
                    'name': page_name,
                    'content_current': mediawiki_page_content,
                    'content_change': page_content
                })
        else:
            changes['pages']['create'].append({
                'name': page_name,
                'content_change': page_content
            })

        keep_page_names.append(page_name.lower())

        progress_bar.update()

    subsidies_category = mediawiki.site.categories[get_subsidies_category_name(mediawiki.lang)]
    for page in subsidies_category.members():
        if page.name.lower() not in keep_page_names:
            changes['pages']['delete'].append({
                'name': page.name,
                'content_current': page.text()
            })

    # Subsidies overview

    page = prepare_subsidies_overview_page(empire_data, mediawiki.lang)

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


def prepare_subsidy_page(subsidy, payments_by_subsidy, sources_by_subsidy, lang, subsidy_template):
    payments = payments_by_subsidy.get(subsidy.database_identifier, [])
    sources = sources_by_subsidy.get(subsidy.database_identifier, [])

    payments_sum = 0.0
    for payment in payments:
        if payment.amount_in_eur:
            payments_sum += payment.amount_in_eur

    return render_prepared_template(lang, 'subsidy.mako', subsidy_template, {
        'subsidy': subsidy,
        'payments': payments,
        'payments_sum': payments_sum,
        'sources': sources
    })


def prepare_subsidies_overview_page(empire_data, lang):
    sorted_subsidies = sorted(
        empire_data.get('subsidies', []), key=lambda s: s.database_identifier)

    subsidies_by_country_dict = {}

    for subsidy in sorted_subsidies:
        if not subsidy.receiving_legal_entity.country in subsidies_by_country_dict:
            subsidies_by_country_dict[subsidy.receiving_legal_entity.country] = []

        subsidies_by_country_dict[subsidy.receiving_legal_entity.country].append(subsidy)

    countries_in_other_group = get_countries_in_other_group(empire_data)

    subsidies_by_country = []
    other_countries_item = {
        'country_name': 'Other countries',
        'subsidies': []
    }

    for country_code, subsidies in subsidies_by_country_dict.items():
        if country_code in countries_in_other_group:
            other_countries_item['subsidies'] += subsidies
        else:
            subsidies_by_country.append({
                'country_code': country_code,
                'country_name': countries.get(country_code).name,
                'subsidies': subsidies
            })

    subsidies_by_country = sorted(
        subsidies_by_country, key=lambda group: group['country_name'])

    if len(other_countries_item['subsidies']) > 0:
        subsidies_by_country.append(other_countries_item)

    stats_by_subsidy = {}
    for subsidy in sorted_subsidies:
        total_amount_in_eur = 0.0
        for payment in (p for p in empire_data.get('subsidies_payments', []) if p.subsidy == subsidy):
            if payment.amount_in_eur:
                total_amount_in_eur += payment.amount_in_eur

        stats_by_subsidy[subsidy.database_identifier] = {
            'total_amount_in_eur': total_amount_in_eur
        }

    return render_page_template(lang, 'subsidies_overview.mako', {
        'subsidies_by_country': subsidies_by_country,
        'stats_by_subsidy': stats_by_subsidy
    })


def get_subsidies_category_name(lang):
    return {
        'en': 'Subsidies',
        'cs': 'Dotace / Subsidies'
    }[lang]
