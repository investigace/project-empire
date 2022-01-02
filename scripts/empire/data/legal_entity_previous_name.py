from dataclasses import dataclass

from .legal_entity import LegalEntity


@dataclass
class LegalEntityPreviousName:
    legal_entity: LegalEntity
    previous_name: str
    named_since_date: str = None
    named_until_date: str = None
