from app.tag.entity.tag import Tag
from app.tag.use_case.dto.delete_tag_dto import DeleteTagDto
from app.tag.use_case.dto.get_tag_search import TagSearch
from app.tag.use_case.tag_repository import ITagRepository


class TagService:
    def __init__(self, repository: ITagRepository):
        self.tag_repository_object = repository

    def get_all(self):
        return self.tag_repository_object.get_all()

    def get_paging(self, tag_search: TagSearch):
        return self.tag_repository_object.get_paging(tag_search)

    def get_tag_category(self):
        return self.tag_repository_object.get_all_category()

    def save_tag(self, tag_model: Tag):
        if tag_model.id is None:
            if self._is_exists_tag_name(tag_model.tag):
                raise ValueError('tag is already exists')

            self.tag_repository_object.insert(tag_model)
        else:
            self.tag_repository_object.update(tag_model)

    def delete_tag(self, delete_dto: DeleteTagDto):
        self.tag_repository_object.delete(delete_dto)

    def _is_exists_tag_name(self, tag_name):
        tag_orm = self.tag_repository_object.get_by_name(tag_name)
        if tag_orm is None:
            return False
        return True
