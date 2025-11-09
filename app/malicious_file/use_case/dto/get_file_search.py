import dataclasses


@dataclasses.dataclass
class FileSearch:
    search_text: str
    category: str
    current_page: int
    page_size: int