from dataclasses import dataclass
from typing import Union

from .legal_entity import LegalEntity
from .person import Person


@dataclass
class OtherRelationship:
    legal_entity: LegalEntity
    related_type: str
    related_name: str
    related_country: str = None
    related_legal_entity_or_person: Union[LegalEntity, Person] = None
    related_address: str = None
    related_legal_entity_identification_number: str = None
    related_person_date_of_birth: str = None

    related_since_date: str = None
    related_until_date: str = None

    relationship_details: str = None
