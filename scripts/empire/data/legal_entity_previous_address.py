from dataclasses import dataclass

from .legal_entity import LegalEntity


@dataclass
class LegalEntityPreviousAddress:
    legal_entity: LegalEntity
    previous_address: str
    address_since_date: str = None
    address_until_date: str = None
