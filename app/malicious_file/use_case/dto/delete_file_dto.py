import dataclasses
from typing import Optional


@dataclasses.dataclass
class DeleteFileDto:
    id: Optional[str]
