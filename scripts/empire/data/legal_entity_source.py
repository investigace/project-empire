from dataclasses import dataclass

from .legal_entity import LegalEntity


@dataclass
class LegalEntitySource:
    legal_entity: LegalEntity
    summary: str = None
    information_gained_from_source: str = None
    last_checked_date: str = None
    url: str = None
