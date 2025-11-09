from abc import abstractmethod

from common.dto.paging import Paging
from app.tag.entity.tag import Tag
from app.tag.use_case.dto.delete_tag_dto import DeleteTagDto
from app.tag.use_case.dto.get_tag_search import TagSearch
from app.tag.use_case.dto.tag_category import TagCategoryDto


class ITagRepository:

    @abstractmethod
    def get_all(self) -> list[Tag] | None:
        pass

    @abstractmethod
    def get_paging(self, tag_search: TagSearch) -> Paging:
        pass

    @abstractmethod
    def get_all_category(self) -> list[TagCategoryDto]:
        pass

    @abstractmethod
    def get_by_name(self, tag_name) -> Tag | None:
        pass

    @abstractmethod
    def get_by_id(self, tag_id) -> Tag | None:
        pass

    @abstractmethod
    def update(self, tag_model: Tag):
        pass

    @abstractmethod
    def insert(self, tag_model: Tag):
        pass

    @abstractmethod
    def delete(self, delete_model: DeleteTagDto):
        pass
