from pprint import pprint

from iso3166 import countries

from .countries import get_countries_in_other_group
from .page_templates import render_page_template


def prepare_people_changes(mediawiki, empire_data):
    changes = {
        'pages': {
            'create': [],
            'update': [],
            'delete': []
        }
    }

    # People pages

    keep_page_names = []

    for person in empire_data.get('people', []):
        page = prepare_person_page(person, empire_data, mediawiki.lang)
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

    people_category = mediawiki.site.categories[get_people_category_name(mediawiki.lang)]
    for page in people_category.members():
        if page.name.lower() not in keep_page_names:
            changes['pages']['delete'].append({
                'name': page.name,
                'content_current': page.text()
            })

    # People overview

    page = prepare_people_overview_page(empire_data, mediawiki.lang)

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


def prepare_person_page(person, empire_data, lang):
    owning = list(o for o in empire_data['owners'] if o.owner_legal_entity_or_person == person)
    other_relationships = list(r for r in empire_data['other_relationships'] if r.related_legal_entity_or_person == person)
    sources = list(s for s in empire_data['people_sources'] if s.person == person)

    owning = sorted(owning, key=lambda o: o.owned_legal_entity.name)
    other_relationships = sorted(other_relationships, key=lambda o: o.legal_entity.name)

    return render_page_template(lang, 'person.mako', {
        'person': person,
        'owning': owning,
        'other_relationships': other_relationships,
        'year_of_birth': person.date_of_birth.strftime('%Y') if person.date_of_birth is not None else None,
        'sources': sources
    })


def prepare_people_overview_page(empire_data, lang):
    people_by_country_dict = {}

    for person in empire_data.get('people', []):
        if not person.nationality in people_by_country_dict:
            people_by_country_dict[person.nationality] = []

        people_by_country_dict[person.nationality].append(person)

    countries_in_other_group = get_countries_in_other_group(empire_data)

    people_by_country = []
    other_countries_item = {
        'country_name': 'Other countries',
        'people': []
    }

    for country_code, people in people_by_country_dict.items():
        if country_code in countries_in_other_group:
            other_countries_item['people'] += people
        else:
            people_by_country.append({
                'country_code': country_code,
                'country_name': countries.get(country_code).name,
                'people': people
            })

    people_by_country = sorted(
        people_by_country, key=lambda group: group['country_name'])

    if len(other_countries_item['people']) > 0:
        people_by_country.append(other_countries_item)

    return render_page_template(lang, 'people_overview.mako', {'people_by_country': people_by_country})

def get_people_category_name(lang):
    return {
        'en': 'People',
        'cs': 'Fyzické osoby / People'
    }[lang]
