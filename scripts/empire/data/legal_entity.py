from dataclasses import dataclass


@dataclass
class LegalEntity:
    database_identifier: str
    legal_entity_type: str
    name: str
    country: str
    identification_number: str = None
    address: str = None
    foundation_date: str = None
    dissolution_date: str = None
    other_notes: str = None
