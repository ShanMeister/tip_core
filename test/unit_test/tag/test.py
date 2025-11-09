import uuid
from datetime import datetime

from app.common.dto.paging import Paging
from app.tag.entity.tag import Tag
from app.tag.use_case.dto.delete_tag_dto import DeleteTagDto
from app.tag.use_case.dto.get_tag_search import TagSearch
from app.tag.use_case.dto.tag_category import TagCategoryDto
from app.tag.use_case.tag_repository import ITagRepository
from app.tag.use_case.tag_service import TagService


class TagRepositoryFake(ITagRepository):

    def __init__(self):
        fake_data_1 = Tag(id=str(uuid.uuid4()),
                          tag='ubuntu',
                          category='os',
                          created_date=datetime.now(),
                          modify_date=datetime.now())

        fake_data_2 = Tag(id=str(uuid.uuid4()),
                          tag='iphone',
                          category='mobile',
                          created_date=datetime.now(),
                          modify_date=datetime.now())

        fake_data_3 = Tag(id=str(uuid.uuid4()),
                          tag='centos',
                          category='os',
                          created_date=datetime.now(),
                          modify_date=datetime.now())

        self.tag_list = []
        self.tag_list.append(fake_data_1)
        self.tag_list.append(fake_data_3)
        self.tag_list.append(fake_data_2)

    def get_all(self) -> list[Tag] | None:
        return self.tag_list

    def get_paging(self, tag_search: TagSearch) -> Paging:
        return Paging(current_page=1, page_size=1000, total_item=len(self.tag_list), items=self.tag_list)

    def get_by_name(self, tag_name) -> Tag | None:
        item_list = [item for item in self.tag_list if tag_name == item.tag]
        if len(item_list) == 0:
            return None

        if len(item_list) > 1:
            raise ValueError

        return item_list[0]

    def get_by_id(self, tag_id) -> Tag | None:
        item_list = [item for item in self.tag_list if tag_id == item.id]
        if len(item_list) == 0:
            return None

        if len(item_list) > 1:
            raise ValueError

        return item_list[0]

    def update(self, tag_model: Tag):
        for item in self.tag_list:
            if tag_model.id == item.id:
                item.modify_date = datetime.now()
                item.tag = tag_model.tag
                item.category = tag_model.category

    def insert(self, tag_model: Tag):
        tag_model.id = str(uuid.uuid4())
        tag_model.created_date = datetime.now()
        tag_model.modify_date = datetime.now()
        self.tag_list.append(tag_model)

    def delete(self, delete_model: DeleteTagDto):
        self.tag_list = [item for item in self.tag_list if item.id != delete_model.id]

    def get_all_category(self) -> list[TagCategoryDto]:
        tag_unique = list({item.category for item in self.tag_list})
        return [TagCategoryDto(category=item) for item in tag_unique]


fake_repository = TagRepositoryFake()
use_case_object = TagService(fake_repository)


def test_get_category():
    tag_category = use_case_object.get_tag_category()
    assert 2 == len(tag_category)


def test_update_tag():
    data_list = use_case_object.get_all()
    fake_data = Tag(id=data_list[0].id,
                    tag='rocky',
                    category='good_os',
                    created_date=None,
                    modify_date=None)

    use_case_object.save_tag(fake_data)
    data_list = use_case_object.get_all()
    current_data = data_list[0]
    assert 3 == len(data_list)
    assert 'rocky' == current_data.tag
    assert 'good_os' == current_data.category


def test_insert_tag():
    fake_data = Tag(id=None,
                    tag='alpine',
                    category='os',
                    created_date=None,
                    modify_date=None)

    use_case_object.save_tag(fake_data)
    data_list = use_case_object.get_all()
    assert 4 == len(data_list)
    data = data_list[3]
    assert 'alpine' == data.tag
    assert 'os' == data.category


def test_repeat_insert_tag():
    fake_data = Tag(id=None,
                    tag='alpine',
                    category='os',
                    created_date=None,
                    modify_date=None)
    try:
        use_case_object.save_tag(fake_data)
        assert False
    except ValueError as e:
        # repeat tag throw ValueError
        assert True


def test_delete_tag():
    data_list = use_case_object.get_all()
    need_delete_data = data_list[0]

    use_case_object.delete_tag(DeleteTagDto(id=need_delete_data.id))
    tag = fake_repository.get_by_id(need_delete_data.id)
    assert None == tag
