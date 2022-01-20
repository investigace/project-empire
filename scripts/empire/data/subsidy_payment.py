from dataclasses import dataclass

from .subsidy import Subsidy


@dataclass
class SubsidyPayment:
    subsidy: Subsidy
    provider: str = None
    year: str = None
    original_currency: str = None
    amount_in_original_currency: float = None
    amount_in_eur: float = None
    notes: str = None

