from dataclasses import dataclass

from .legal_entity import LegalEntity


@dataclass
class LegalEntityMediaMention:
    legal_entity: LegalEntity
    summary: str = None
    last_checked_date: str = None
    url: str = None
