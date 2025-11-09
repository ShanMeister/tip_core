import dataclasses


@dataclasses.dataclass
class Paging:
    current_page: int
    page_size: int
    total_item: int
    items: object
    total_page: int = dataclasses.field(default=0)

    def __post_init__(self):
        self.calculate_total_page()

    def calculate_total_page(self):
        self.total_page = (self.total_item + self.page_size - 1) // self.page_size
