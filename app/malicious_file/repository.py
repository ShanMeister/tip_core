import uuid
import re
import json

from django.core.paginator import Paginator
from django_elasticsearch_dsl import Index
from elasticsearch_dsl import Q, A
from virus_total_apis import PublicApi as VirusTotalPublicApi
from common.dto.paging import Paging
from stix2 import Indicator, ExternalReference, ExtensionDefinition, Bundle

from app.stix.repository.stix2_repository_elastic import StixDomainObjectDocument
from app.malicious_file.use_case.dto.file_name import FileNameDto
from app.malicious_file.use_case.dto.get_file_search import FileSearch
from app.stix.repository.stix2_repository_elastic import Stix2RepositoryElastic
from app.malicious_file.use_case.dto.delete_file_dto import DeleteFileDto

stix_repo_object = Stix2RepositoryElastic()
API_KEY = ""
vt = VirusTotalPublicApi(API_KEY)

MARKING_EXTENSION_ID = 'extension-definition--84971988-6031-4666-864a-64e5b15bb8cc'
EXTENSION_TYPE = 'property-extension'

extension_definition = ExtensionDefinition(
    spec_version= "2.1",
    name= "Extension apwg",
    description= "Extension for apwg property",
    created= "2024-05-31T09:37:13.650111Z",
    modified= "2024-05-31T09:37:13.650111Z",
    created_by_ref= "identity--18dc2b30-5c46-4cd8-8a53-2024b88a66c2",
    version= "1.2.1",
    schema= "https://no.domain.com",
    extension_types= [EXTENSION_TYPE],
)


def get_vt_report(file_hash: str):
    report = vt.get_file_report(file_hash)
    if 'results' in report and report["response_code"] == 200:
        # scan_date = datetime.strptime(report['results']['scan_date'], '%Y-%m-%d %H:%M:%S')
        response_data = {
            'md5': report['results']['md5'],
            'malicious': report['results']['positives'],
            'resource': report['results']['resource'],
            'response_code': report['results']['response_code'],
            'scan_date': report['results']['scan_date'],
            'total': report['results']['total']
        }
    else:
        response_data = None
        print('Fetch data fail')
    return response_data


def data_to_indicator(response_data: dict) -> Indicator | None:
    try:
        indicator = Indicator(
            name="VirusTotal Indicator",
            description="Indicator generated from VirusTotal intelligence",
            pattern=f"[file:hashes.\'MD5\' = '{response_data['md5']}']",
            pattern_type="stix",
            valid_from=response_data['scan_date'],  # Set the observed date as the valid_from timestamp
            external_references=[ExternalReference(
                source_name="VirusTotal",
                url="https://www.virustotal.com/"
            )],
            extensions={
                MARKING_EXTENSION_ID: {
                    'extension_type': EXTENSION_TYPE,
                    'malicious_amount': response_data['malicious'],
                    'resource': response_data['resource'],
                    'total': response_data['total'],
                    'last_seen': [scan_date],
                    'valid_from': None,
                }}
        )
        return indicator
    except Exception as e:
        print(e)
        return None


def stix_to_bundle(indicator) -> Bundle:
    stix_bundle = Bundle(objects=indicator)
    return stix_bundle


class MaliciousFileRepository:
    orm_search = StixDomainObjectDocument.search()
    refresh_index = Index('stix_domain_object')

    @staticmethod
    def get_all_files():
        search = StixDomainObjectDocument.search().query("match_all")
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
    def save_file(file_hash, file_name, tag):
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
        try:
            # report = get_vt_report(file_hash)
            report = {'md5': '89e55fe505754e20ec217f0a2b85092b', 'malicious': 1, 'resource': '3055bf9c65eb958a8e9bf9f5c061a629deace0a608334ae7725e8c6b26f4d554', 'response_code': 1, 'scan_date': '2024-03-15 09:53:29', 'total': 62}
            file_indicator = data_to_indicator(report)
            # file_bundle = stix_to_bundle(file_indicator)
            if file_indicator:
                indicator_dict = json.loads(file_indicator.serialize())
                stix_repo_object.save_indicator(indicator_dict)
            else:
                print('No data report to save.')
        except Exception as e:
            print(e)

    @staticmethod
    def delete_file(delete_dto: DeleteFileDto):
        search = MaliciousFileRepository.orm_search.filter("term", id=delete_dto.id)
        response = search.execute()
        if response.hits.total.value > 0:
            response.hits[0].delete()
            MaliciousFileRepository.refresh_self_index()

    @staticmethod
    def refresh_self_index():
        MaliciousFileRepository.refresh_index.refresh()

    def get_all_name(self) -> list[FileNameDto]:
        terms_agg = A('terms', field='name')

        # unique_values -> self define naming
        self.orm_search.aggs.bucket('unique_values', terms_agg)

        response = self.orm_search.execute(ignore_cache=True)
        rule_name_list = [FileNameDto(name=bucket.key) for bucket in
                             response.aggregations.unique_values.buckets]

        return rule_name_list

    def get_paging(self, file_search: FileSearch) -> Paging:
        query_filter = []

        if file_search.category:
            query_filter.append(Q("term", name=file_search.category))
        query_filter.append(Q("wildcard", pattern=f"*{file_search.search_text}*"))

        s = self.orm_search.filter("bool", must=query_filter)

        page_size = file_search.page_size
        page_num = file_search.current_page

        paginator = Paginator(s, page_size)
        page = paginator.page(page_num)

        # 獲取分頁數據
        results = page.object_list.execute()
        # data = [hit.to_dict() for hit in results]
        data = []
        for hit in results:
            hit_dict = hit.to_dict()
            match = re.search(r"=\s*'([^']*)'", hit_dict['pattern'])
            if match:
                extracted_hash = match.group(1)
            else:
                extracted_hash = None

            date_dict = {
                'id': hit_dict['id'],
                'hash': extracted_hash,
                'name': hit_dict['name'],
                'author': 'daniel',
                'create_time': hit_dict['valid_from']
            }
            data.append(date_dict)
        paging = Paging(current_page=page_num, page_size=page_size, total_item=results.hits.total.value, items=data)

        return paging
