def get_countries_in_other_group(empire_data):
    legal_entities_by_country = {}

    for legal_entity in empire_data.get('legal_entities', []):
        if not legal_entity.country in legal_entities_by_country:
            legal_entities_by_country[legal_entity.country] = 0

        legal_entities_by_country[legal_entity.country] += 1

    people_by_country = {}

    for person in empire_data.get('people', []):
        if not person.nationality in people_by_country:
            people_by_country[person.nationality] = 0

        people_by_country[person.nationality] += 1

    all_countries = list(set(list(legal_entities_by_country.keys()) + list(people_by_country.keys())))
    countries_in_other_group = []

    for country in all_countries:
        if legal_entities_by_country.get(country, 0) < 5 and people_by_country.get(country, 0) < 5:
            countries_in_other_group.append(country)

    return countries_in_other_group
