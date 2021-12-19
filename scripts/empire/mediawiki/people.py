from pprint import pprint
from os.path import join, dirname

from iso3166 import countries
from mako.template import Template


def prepare_people_changes(site, empire_data):
    changes = {
        'pages': {
            'create': [],
            'update': [],
            'delete': []
        }
    }

    # People pages

    if 'people' in empire_data:
        keep_page_names = []

        for person in empire_data['people']:
            page_name = person.database_identifier
            page_content = build_person_page_content(person)

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

        people_category = site.categories['People']
        for page in people_category.members():
            if page.name.lower() not in keep_page_names:
                changes['pages']['delete'].append({
                    'name': page.name,
                    'content_current': page.text()
                })

    # People overview

    overview_page_name = 'People overview'

    if 'people' in empire_data:
        people_by_country_dict = {}

        for person in empire_data['people']:
            if not person.nationality in people_by_country_dict:
                people_by_country_dict[person.nationality] = []

            people_by_country_dict[person.nationality].append(person)

        people_by_country = []
        for country_code, people in people_by_country_dict.items():
            people_by_country.append({
                'country_code': country_code,
                'country_name': countries.get(country_code).name,
                'people': people
            })

        people_by_country = sorted(people_by_country, key=lambda group: group['country_name'])

        page_content = build_people_overview_page_content(people_by_country)

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


def build_person_page_content(person):
    template = Template(filename=join(dirname(__file__), 'page_templates', 'person.mako'))

    return template.render(person=person).strip()


def build_people_overview_page_content(people_by_country):
    template = Template(filename=join(dirname(__file__), 'page_templates', 'people_overview.mako'))

    return template.render(people_by_country=people_by_country).strip()
