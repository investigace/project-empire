from dataclasses import dataclass
from typing import Union

from .legal_entity import LegalEntity
from .person import Person


@dataclass
class Owner:
    owned_legal_entity: LegalEntity
    owner_type: str
    owner_name: str
    owner_country: str = None
    owner_legal_entity_or_person: Union[LegalEntity, Person] = None
    owner_address: str = None
    owner_legal_entity_identification_number: str = None
    owner_person_date_of_birth: str = None
    
    owned_percentage: str = None
    owned_since_date: str = None
    owned_until_date: str = None

    ownership_details: str = None
