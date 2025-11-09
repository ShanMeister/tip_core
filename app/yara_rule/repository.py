from django.shortcuts import get_object_or_404
from datetime import datetime
from django_elasticsearch_dsl import fields
from elasticsearch.exceptions import NotFoundError
import uuid

from django.core.paginator import Paginator
from django_elasticsearch_dsl import Index
from elasticsearch_dsl import Q, A

from common.dto.paging import Paging
from app.yara_rule.documents import YaraRuleModelDocument
from app.yara_rule.use_case.dto.yara_rule_name import YaraRuleNameDto
from app.yara_rule.use_case.dto.get_name_search import NameSearch


class YaraRuleRepository:
    orm_search = YaraRuleModelDocument.search()
    refresh_index = Index('cht_tip_yara-rule')

    @staticmethod
    def get_all_yara_rules():
        search = YaraRuleModelDocument.search().query("match_all").sort("-modify_date")
        response = search.execute()
        if response is None:
            return None
        # data = [hit.to_dict() for hit in response]
        data = []

        for hit in response:
            hit_dict = hit.to_dict()
            if 'tag' in hit_dict:
                hit_dict['tag'] = hit_dict['tag']['tag']
            data.append(hit_dict)
        return data

    @staticmethod
    def save_yara_rule(name, tag, rule_content):
        tag_data = {
            'id': uuid.uuid4(),
            'tag': tag,
            'category': 'example-category'
        }

        author_data = {
            'id': uuid.uuid4(),
            'name': 'daniel',
            'email': 'example@chtsecurity.com'
        }

        # Save to Elasticsearch and database through the document's save method
        yara_document = YaraRuleModelDocument(
            id=uuid.uuid4(),
            name=name,
            tag=tag_data,
            rule_content=rule_content,
            created_date=datetime.now(),
            modify_date=datetime.now(),
            author=author_data
        )
        yara_document.save()
        return yara_document

    @staticmethod
    def delete_yara_rule(rule_id):
        search = YaraRuleRepository.orm_search.filter("term", id=rule_id)
        response = search.execute()
        if response.hits.total.value > 0:
            response.hits[0].delete()
            YaraRuleRepository.refresh_self_index()

    @staticmethod
    def refresh_self_index():
        YaraRuleRepository.refresh_index.refresh()

    def get_by_id(self, tag_id):
        if id is None:
            return None

        search = self.orm_search.filter("term", id=tag_id)
        response = search.execute()
        if response.hits.total.value > 0:
            return response.hits[0]

        return None

    def get_all_name(self) -> list[YaraRuleNameDto]:
        terms_agg = A('terms', field='name')

        # unique_values -> self define naming
        self.orm_search.aggs.bucket('unique_values', terms_agg)

        response = self.orm_search.execute(ignore_cache=True)
        rule_name_list = [YaraRuleNameDto(name=bucket.key) for bucket in
                             response.aggregations.unique_values.buckets]

        return rule_name_list

    def get_paging(self, name_search: NameSearch) -> Paging:
        query_filter = []

        if name_search.category:
            query_filter.append(Q("term", name=name_search.category))
        query_filter.append(Q("wildcard", name=f"*{name_search.search_text}*"))

        s = self.orm_search.filter("bool", must=query_filter) \
            .sort("-modify_date")

        page_size = name_search.page_size
        page_num = name_search.current_page

        paginator = Paginator(s, page_size)
        page = paginator.page(page_num)

        # 獲取分頁數據
        results = page.object_list.execute()
        data = [hit.to_dict() for hit in results]

        paging = Paging(current_page=page_num, page_size=page_size, total_item=results.hits.total.value, items=data)

        return paging


