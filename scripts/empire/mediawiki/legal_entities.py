from pprint import pprint

from iso3166 import countries

from .countries import get_countries_in_other_group
from .page_templates import render_page_template


def prepare_legal_entities_changes(mediawiki, empire_data):
    changes = {
        'pages': {
            'create': [],
            'update': [],
            'delete': []
        }
    }

    # wanted_categories = [
    #     'Legal entities'
    # ]

    # if 'legal_entities' in empire_data:
    #     types = map(lambda legal_entity: legal_entity.legal_entity_type, empire_data['legal_entities'])
    #     types = list(set(types)) # unique
    #     types = filter(lambda type: type is not None, types)

    #     for type in types:
    #         wanted_categories.append(f'Legal entity type {type}')

    # existing_categories = list(map(lambda cat: cat.name[9:], list(mediawiki.site.allcategories())))

    # pprint(existing_categories)
    # pprint(wanted_categories)

    # Legal entities pages

    keep_page_names = []

    for legal_entity in empire_data.get('legal_entities', []):
        page = prepare_legal_entity_page(legal_entity, mediawiki.lang)
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

    legal_entities_category = mediawiki.site.categories[get_legal_entities_category_name(mediawiki.lang)]
    for page in legal_entities_category.members():
        if page.name.lower() not in keep_page_names:
            changes['pages']['delete'].append({
                'name': page.name,
                'content_current': page.text()
            })

    # Legal entities overview

    page = prepare_legal_entities_overview_page(empire_data, mediawiki.lang)
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

    return changes


def prepare_legal_entity_page(legal_entity, lang):
    return render_page_template(lang, 'legal_entity.mako', {'legal_entity': legal_entity})


def prepare_legal_entities_overview_page(empire_data, lang):
    legal_entities_by_country_dict = {}

    for legal_entity in empire_data.get('legal_entities', []):
        if not legal_entity.country in legal_entities_by_country_dict:
            legal_entities_by_country_dict[legal_entity.country] = []

        legal_entities_by_country_dict[legal_entity.country].append(
            legal_entity)

    countries_in_other_group = get_countries_in_other_group(empire_data)

    legal_entities_by_country = []
    other_countries_item = {
        'country_name': 'Other countries',
        'legal_entities': []
    }

    for country_code, legal_entities in legal_entities_by_country_dict.items():
        if country_code in countries_in_other_group:
            other_countries_item['legal_entities'] += legal_entities
        else:
            legal_entities_by_country.append({
                'country_code': country_code,
                'country_name': countries.get(country_code).name,
                'legal_entities': legal_entities
            })

    legal_entities_by_country = sorted(
        legal_entities_by_country, key=lambda group: group['country_name'])

    if len(other_countries_item['legal_entities']) > 0:
        legal_entities_by_country.append(other_countries_item)

    return render_page_template(lang, 'legal_entities_overview.mako', {'legal_entities_by_country': legal_entities_by_country})

def get_legal_entities_category_name(lang):
    return {
        'en': 'Legal entities',
        'cs': 'Právnické osoby / Legal entities'
    }[lang]
