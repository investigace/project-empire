import locale
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

    # Legal entities pages

    keep_page_names = []

    for legal_entity in empire_data.get('legal_entities', []):
        page = prepare_legal_entity_page(legal_entity, empire_data, mediawiki.lang)
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


def prepare_legal_entity_page(legal_entity, empire_data, lang):
    def map_owner(owner):
        info_line_items = [owner.owner_name, owner.owner_type]
        if owner.owner_country:
            info_line_items.append(owner.owner_country)
        if owner.owner_address:
            info_line_items.append(owner.owner_address)
        if owner.owner_legal_entity_identification_number:
            info_line_items.append(owner.owner_legal_entity_identification_number)
        if owner.owner_person_date_of_birth:
            info_line_items.append(str(owner.owner_person_date_of_birth))

        return {
            **vars(owner),
            'info_line': ', '.join(info_line_items)
        }

    def map_other_relationship(other_relationship):
        info_line_items = [other_relationship.related_name, other_relationship.related_type]
        if other_relationship.related_country:
            info_line_items.append(other_relationship.related_country)
        if other_relationship.related_address:
            info_line_items.append(other_relationship.related_address)
        if other_relationship.related_legal_entity_identification_number:
            info_line_items.append(other_relationship.related_legal_entity_identification_number)
        if other_relationship.related_person_date_of_birth:
            info_line_items.append(str(other_relationship.related_person_date_of_birth))

        return {
            **vars(other_relationship),
            'info_line': ', '.join(info_line_items)
        }

    owners = list(map(map_owner, (o for o in empire_data['owners'] if o.owned_legal_entity == legal_entity)))
    owning = list(o for o in empire_data['owners'] if o.owner_legal_entity_or_person == legal_entity)
    other_relationships = list(map(map_other_relationship, (r for r in empire_data['other_relationships'] if r.legal_entity == legal_entity)))
    previous_names = list(pn for pn in empire_data['legal_entities_previous_names'] if pn.legal_entity == legal_entity)
    previous_addresses = list(pn for pn in empire_data['legal_entities_previous_addresses'] if pn.legal_entity == legal_entity)
    media_mentions = list(m for m in empire_data['legal_entities_media_mentions'] if m.legal_entity == legal_entity)
    sources = list(s for s in empire_data['legal_entities_sources'] if s.legal_entity == legal_entity)

    empty_date_first = lambda date: str(date) if date is not None else '9999'
    owners = sorted(owners, key=lambda o: (empty_date_first(o['owned_until_date']), empty_date_first(o['owned_since_date'])), reverse=True)
    owning = sorted(owning, key=lambda o: locale.strxfrm(o.owned_legal_entity.name))
    other_relationships = sorted(other_relationships, key=lambda r: locale.strxfrm(r['related_name']))
    previous_names = sorted(previous_names, key=lambda pn: (empty_date_first(pn.named_until_date), empty_date_first(pn.named_since_date)), reverse=True)
    previous_addresses = sorted(previous_addresses, key=lambda pa: (empty_date_first(pa.address_until_date), empty_date_first(pa.address_since_date)), reverse=True)

    return render_page_template(lang, 'legal_entity.mako', {
        'legal_entity': legal_entity,
        'owners': owners,
        'owning': owning,
        'other_relationships': other_relationships,
        'previous_names': previous_names,
        'previous_addresses': previous_addresses,
        'media_mentions': media_mentions,
        'sources': sources
    })


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
