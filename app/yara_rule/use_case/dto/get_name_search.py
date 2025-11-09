import dataclasses


@dataclasses.dataclass
class NameSearch:
    search_text: str
    category: str
    current_page: int
    page_size: int