from pprint import pprint

from ..data import Person


def link_fetched_relationships(current_empire_data, fetched_empire_data):
    result = {
        **fetched_empire_data,
        'people': []
    }

    people_by_name_and_dob = {}
    for person in current_empire_data['people']:
        key = (person.full_name.lower(), person.date_of_birth)
        people_by_name_and_dob[key] = person

    legal_entities_by_country_and_identification = {}
    for legal_entity in current_empire_data['legal_entities']:
        if legal_entity.identification_number:
            key = (legal_entity.country, str(legal_entity.identification_number))
            legal_entities_by_country_and_identification[key] = legal_entity


    relationships_by_name_and_dob = {}

    for owner in fetched_empire_data['legal_entities_owners']:
        if owner.owner_type == 'Person':
            key = (owner.owner_name.lower(), owner.owner_person_date_of_birth)

            if key in people_by_name_and_dob:
                # Found existing person, link and continue
                owner.owner_legal_entity_or_person = people_by_name_and_dob[key]
                continue
            else:
                # Not found existing person, add the owner to the keyed list
                if key not in relationships_by_name_and_dob:
                    relationships_by_name_and_dob[key] = {
                        'owners': [],
                        'other_relationships': []
                    }
                relationships_by_name_and_dob[key]['owners'].append(owner)

    for other_relationship in fetched_empire_data['legal_entities_other_relationships']:
        if other_relationship.related_type == 'Person':
            key = (other_relationship.related_name.lower(), other_relationship.related_person_date_of_birth)

            if key in people_by_name_and_dob:
                # Found existing person, link and continue
                other_relationship.related_legal_entity_or_person = people_by_name_and_dob[key]
                continue
            else:
                # Not found existing person, add the other rel. to the keyed list
                if key not in relationships_by_name_and_dob:
                    relationships_by_name_and_dob[key] = {
                        'owners': [],
                        'other_relationships': []
                    }
                relationships_by_name_and_dob[key]['other_relationships'].append(other_relationship)


    used_database_identifiers = list(map(lambda p: p.database_identifier, current_empire_data['people']))

    for key, relationships in relationships_by_name_and_dob.items():
        recent_owners = sorted(relationships['owners'], key=lambda o: str(o.owned_since_date), reverse=True)
        recent_other_relationships = sorted(relationships['other_relationships'], key=lambda r: str(r.related_since_date), reverse=True)

        if len(recent_owners) > 0:
            owner = recent_owners[0]

            person_data = {
                'database_identifier': owner.owner_name,
                'full_name': owner.owner_name,
                'nationality': owner.owner_country,
                'date_of_birth': owner.owner_person_date_of_birth,
                'residence_country': owner.owner_country,
                'residence_address': owner.owner_address,
                'residence_city': '',
                'other_notes': ''
            }
        else:
            other_relationship = recent_other_relationships[0]

            person_data = {
                'database_identifier': other_relationship.related_name,
                'full_name': other_relationship.related_name,
                'nationality': other_relationship.related_country,
                'date_of_birth': other_relationship.related_person_date_of_birth,
                'residence_country': other_relationship.related_country,
                'residence_address': other_relationship.related_address,
                'residence_city': '',
                'other_notes': ''
            }

        person = Person(**person_data)

        num = 2
        while person.database_identifier in used_database_identifiers:
            person.database_identifier = person.full_name + ' ' + str(num)
            num += 1

        used_database_identifiers.append(person.database_identifier)

        for owner in relationships['owners']:
            owner.owner_legal_entity_or_person = person
        for other_relationship in relationships['other_relationships']:
            other_relationship.related_legal_entity_or_person = person

        result['people'].append(person)


    for owner in fetched_empire_data['legal_entities_owners']:
        if owner.owner_type == 'Legal entity' and owner.owner_legal_entity_identification_number:
            key = (owner.owner_country, str(owner.owner_legal_entity_identification_number))

            if key in legal_entities_by_country_and_identification:
                owner.owner_legal_entity_or_person = legal_entities_by_country_and_identification[key]

    for other_relationship in fetched_empire_data['legal_entities_other_relationships']:
        if other_relationship.related_type == 'Legal entity' and other_relationship.related_legal_entity_identification_number:
            key = (other_relationship.related_country, str(other_relationship.related_legal_entity_identification_number))

            if key in legal_entities_by_country_and_identification:
                other_relationship.related_legal_entity_or_person = legal_entities_by_country_and_identification[key]


    return result
