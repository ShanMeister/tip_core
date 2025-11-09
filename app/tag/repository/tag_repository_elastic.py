import uuid
from datetime import datetime

from django.core.paginator import Paginator
from django_elasticsearch_dsl import Index
from elasticsearch_dsl import Q, A

from app.tag.documents import TagDocument
from app.tag.entity.tag import Tag
from app.tag.use_case.dto.delete_tag_dto import DeleteTagDto
from app.tag.use_case.dto.get_tag_search import TagSearch
from app.tag.use_case.dto.tag_category import TagCategoryDto
from app.tag.use_case.tag_repository import ITagRepository
from app.common.dto.paging import Paging


class TagRepository(ITagRepository):
    orm_search = TagDocument.search()
    refresh_index = Index('cht_tip_tag')

    def get_all(self) -> list[Tag] | None:
        self.orm_search.query("match_all")
        response = self.orm_search.execute()
        if response is None:
            return None

        data = [self.__document_to_entity(hit) for hit in response]
        return data

    def get_paging(self, tag_search: TagSearch) -> Paging:
        query_filter = []

        if tag_search.category:
            query_filter.append(Q("term", category=tag_search.category))
        query_filter.append(Q("wildcard", tag=f"*{tag_search.search_text}*"))

        s = self.orm_search.filter("bool", must=query_filter) \
            .sort("-modify_date")

        page_size = tag_search.page_size
        page_num = tag_search.current_page

        paginator = Paginator(s, page_size)
        page = paginator.page(page_num)

        # 獲取分頁數據
        results = page.object_list.execute()
        data = [hit.to_dict() for hit in results]

        paging = Paging(current_page=page_num, page_size=page_size, total_item=results.hits.total.value, items=data)

        return paging

    def get_all_category(self) -> list[TagCategoryDto]:
        terms_agg = A('terms', field='category')

        # unique_values -> self define naming
        self.orm_search.aggs.bucket('unique_values', terms_agg)

        response = self.orm_search.execute(ignore_cache=True)
        tag_category_list = [TagCategoryDto(category=bucket.key) for bucket in
                             response.aggregations.unique_values.buckets]

        return tag_category_list

    def get_by_name(self, tag_name) -> Tag | None:
        if tag_name is None:
            return None

        search = self.orm_search.filter("term", tag=tag_name)
        response = search.execute()
        if response.hits.total.value > 0:
            return self.__document_to_entity(response.hits[0])

        return None

    def get_by_id(self, tag_id) -> Tag | None:
        if id is None:
            return None

        search = self.orm_search.filter("term", id=tag_id)
        response = search.execute()
        if response.hits.total.value > 0:
            return self.__document_to_entity(response.hits[0])

        return None

    def update(self, tag_model: Tag):
        search = self.orm_search.filter("term", id=tag_model.id)
        response = search.execute()
        if response.hits.total.value > 0:
            existing_product = response.hits[0]
            setattr(existing_product, 'tag', tag_model.tag)
            setattr(existing_product, 'category', tag_model.category)
            setattr(existing_product, 'author', {
                'id': '2',
                'name': 'hao',
                'email': 'zxcv45628789@chtsecurity.com'
            })
            existing_product.save()
            self.__refresh_self_index()

    def insert(self, tag_model: Tag):
        product_document = TagDocument(id=str(uuid.uuid4()), tag=tag_model.tag,
                                       category=tag_model.category,
                                       created_date=datetime.now(), author={
                'id': '1',
                'name': 'xing',
                'email': 'zxcv45628789@chtsecurity.com'
            })
        product_document.save()
        self.__refresh_self_index()

    def delete(self, delete_model: DeleteTagDto):
        search = self.orm_search.filter("term", id=delete_model.id)
        response = search.execute()
        if response.hits.total.value > 0:
            existing_product = response.hits[0]
            existing_product.delete()
            self.__refresh_self_index()

    def __refresh_self_index(self):
        self.refresh_index.refresh()

    def __document_to_entity(self, tag_document: TagDocument) -> Tag:
        return Tag(id=tag_document.id,
                   tag=tag_document.tag,
                   category=tag_document.category,
                   created_date=tag_document.created_date,
                   modify_date=tag_document.modify_date)
