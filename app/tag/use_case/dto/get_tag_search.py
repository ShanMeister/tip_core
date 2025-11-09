import dataclasses


@dataclasses.dataclass
class TagSearch:
    search_text: str
    category: str
    current_page: int
    page_size: int
