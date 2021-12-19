from dataclasses import dataclass


@dataclass
class Person:
    database_identifier: str
    full_name: str
    nationality: str = None
    date_of_birth: str = None
    residence_country: str = None
    residence_address: str = None
    residence_city: str = None
    other_notes: str = None
