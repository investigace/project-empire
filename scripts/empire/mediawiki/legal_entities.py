from pprint import pprint
from os.path import join, dirname

from iso3166 import countries
from mako.template import Template


def prepare_legal_entities_changes(site, empire_data):
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

    # existing_categories = list(map(lambda cat: cat.name[9:], list(site.allcategories())))

    # pprint(existing_categories)
    # pprint(wanted_categories)

    # Legal entities pages

    if 'legal_entities' in empire_data:
        keep_page_names = []

        for legal_entity in empire_data['legal_entities']:
            page_name = legal_entity.database_identifier
            page_content = build_legal_entity_page_content(legal_entity)

            mediawiki_page = site.pages[page_name]

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

        legal_entities_category = site.categories['Legal entities']
        for page in legal_entities_category.members():
            if page.name.lower() not in keep_page_names:
                changes['pages']['delete'].append({
                    'name': page.name,
                    'content_current': page.text()
                })

    # Legal entities overview

    overview_page_name = 'Legal entities overview'

    if 'legal_entities' in empire_data:
        legal_entities_by_country_dict = {}

        for legal_entity in empire_data['legal_entities']:
            if not legal_entity.country in legal_entities_by_country_dict:
                legal_entities_by_country_dict[legal_entity.country] = []

            legal_entities_by_country_dict[legal_entity.country].append(legal_entity)

        legal_entities_by_country = []
        for country_code, legal_entities in legal_entities_by_country_dict.items():
            legal_entities_by_country.append({
                'country_code': country_code,
                'country_name': countries.get(country_code).name,
                'legal_entities': legal_entities
            })

        legal_entities_by_country = sorted(legal_entities_by_country, key=lambda group: group['country_name'])

        page_content = build_legal_entities_overview_page_content(legal_entities_by_country)

        mediawiki_page = site.pages[overview_page_name]

        if mediawiki_page.exists:
            mediawiki_page_content = mediawiki_page.text()

            if mediawiki_page_content != page_content:
                changes['pages']['update'].append({
                    'name': overview_page_name,
                    'content_current': mediawiki_page_content,
                    'content_change': page_content
                })
        else:
            changes['pages']['create'].append({
                'name': overview_page_name,
                'content_change': page_content
            })
    else:
        if site.pages[overview_page_name].exists:
            changes['pages']['delete'].append({
                'name': overview_page_name,
                'content_current': site.pages[overview_page_name].text()
            })

    return changes


def build_legal_entity_page_content(legal_entity):
    template = Template(filename=join(dirname(__file__), 'page_templates', 'legal_entity.mako'))

    return template.render(legal_entity=legal_entity).strip()


def build_legal_entities_overview_page_content(legal_entities_by_country):
    template = Template(filename=join(dirname(__file__), 'page_templates', 'legal_entities_overview.mako'))

    return template.render(legal_entities_by_country=legal_entities_by_country).strip()
