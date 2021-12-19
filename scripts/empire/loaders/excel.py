from datetime import date, datetime
from pprint import pprint

from openpyxl import load_workbook

from ..data import LegalEntity, Person


def load_excel(excel_path):
    wb = load_workbook(filename=excel_path)

    # Load legal entities

    legal_entities_ws = wb['1. Legal entities']

    legal_entities_cols = {
        'Database identifier': 'database_identifier',
        'Legal entity type': 'legal_entity_type',
        'Name': 'name',
        'Country': 'country',
        'Identification number': 'identification_number',
        'Address': 'address',
        'Foundation date': 'foundation_date',
        'Dissolution date': 'dissolution_date',
        'Other notes': 'other_notes'
    }

    legal_entities_cols_numbers = {}

    header_row = legal_entities_ws.iter_rows(min_row=4, max_row=4)
    for cell in list(header_row)[0]:
        for legal_entity_col in legal_entities_cols.keys():
            if cell.value == legal_entity_col:
                legal_entities_cols_numbers[cell.column] = legal_entity_col

    legal_entities = []

    data_rows = legal_entities_ws.iter_rows(min_row=5, max_row=legal_entities_ws.max_row)
    for row in data_rows:
        legal_entity_data = {}

        for cell in row:
            if cell.column in legal_entities_cols_numbers and cell.value is not None:
                legal_entity_col = legal_entities_cols_numbers[cell.column]

                value = cell.value

                if legal_entity_col == 'Foundation date' or legal_entity_col == 'Dissolution date':
                    value = parse_date(value)

                legal_entity_data[legal_entities_cols[legal_entity_col]] = value

        if legal_entity_data:
            legal_entities.append(LegalEntity(**legal_entity_data))

    # Load people

    people_ws = wb['2. People']

    people_cols = {
        'Database identifier': 'database_identifier',
        'Full name': 'full_name',
        'Nationality': 'nationality',
        'Date of birth': 'date_of_birth',
        'Residence country': 'residence_country',
        'Residence full address': 'residence_address',
        'Residence only city': 'residence_city',
        'Other notes': 'other_notes'
    }

    people_cols_numbers = {}

    header_row = people_ws.iter_rows(min_row=4, max_row=4)
    for cell in list(header_row)[0]:
        for people_col in people_cols.keys():
            if cell.value == people_col:
                people_cols_numbers[cell.column] = people_col

    people = []

    data_rows = people_ws.iter_rows(min_row=5, max_row=people_ws.max_row)
    for row in data_rows:
        person_data = {}

        for cell in row:
            if cell.column in people_cols_numbers and cell.value is not None:
                people_col = people_cols_numbers[cell.column]

                value = cell.value

                if people_col == 'Date of birth':
                    value = parse_date(value)

                person_data[people_cols[people_col]] = value

        if person_data:
            people.append(Person(**person_data))

    return {
        'legal_entities': legal_entities,
        'people': people
    }


def parse_date(date_str):
    if date_str == "":
        return None

    if isinstance(date_str, datetime):
        return date_str.date()

    datetime_obj = None

    try:
        datetime_obj = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        pass

    try:
        datetime_obj = datetime.strptime(date_str, '%d.%m.%Y')
    except ValueError:
        pass

    return datetime_obj.date() if datetime_obj else None
