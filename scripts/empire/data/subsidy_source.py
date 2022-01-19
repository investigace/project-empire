from dataclasses import dataclass

from .subsidy import Subsidy


@dataclass
class SubsidySource:
    subsidy: Subsidy
    summary: str = None
    information_gained_from_source: str = None
    last_checked_date: str = None
    url: str = None
