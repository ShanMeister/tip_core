import dataclasses
from datetime import date
from typing import Optional


@dataclasses.dataclass
class Tag:
    id: Optional[str]
    tag: str
    category: str
    created_date: Optional[date]
    modify_date: Optional[date]
