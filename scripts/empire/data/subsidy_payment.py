from dataclasses import dataclass

from .subsidy import Subsidy


@dataclass
class SubsidyPayment:
    subsidy: Subsidy
    amount_in_eur: float
    amount_in_original_currency: float
    original_currency: str
    provider: str = None
    year: str = None
    notes: str = None

