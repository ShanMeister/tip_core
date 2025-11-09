import dataclasses
from typing import Optional


@dataclasses.dataclass
class DeleteTagDto:
    id: Optional[str]
