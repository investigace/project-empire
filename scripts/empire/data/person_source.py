from dataclasses import dataclass

from .person import Person


@dataclass
class PersonSource:
    person: Person
    summary: str = None
    information_gained_from_source: str = None
    last_checked_date: str = None
    url: str = None
