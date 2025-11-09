from django_elasticsearch_dsl import Index
from elasticsearch_dsl import Q
from stix2 import Indicator, parse

from stix.documents import StixDomainObjectDocument, StixMetaObjectDocument
from stix.use_case.stix2_repository_interface import IStix2Repository


class Stix2RepositoryElastic(IStix2Repository):
    sdo_search = StixDomainObjectDocument.search()
    sdo_index = Index('stix_domain_object')

    smo_search = StixMetaObjectDocument.search()
    smo_index = Index('stix_meta_object')

    def find_indicator_by_pattern(self, pattern) -> Indicator | None:
        query_filter = [Q("match", type="indicator"),
                        Q("match_phrase", pattern=pattern)]

        search = self.sdo_search.query("bool", must=query_filter)
        indicator = search.execute()
        if indicator.hits.total.value > 0:
            return self._document_to_stix(indicator.hits[0])

        return None

    def save_indicator(self, indicator_dict: dict):
        indicator = self.__find_sdo_by_id(indicator_dict['id'])

        if indicator is None:
            StixDomainObjectDocument(**indicator_dict).save()
        else:
            indicator.extensions = indicator_dict['extensions']
            indicator.valid_from = indicator_dict['valid_from']
            indicator.modified = indicator_dict['modified']
            indicator.external_references = indicator_dict['external_references']
            indicator.save()

    def save_smo(self, smo_dict: dict):
        pass

    def __find_sdo_by_id(self, Id: str):
        query_filter = [Q("match", id=Id)]
        search = self.sdo_search.query("bool", must=query_filter)
        indicator = search.execute()
        if indicator.hits.total.value > 0:
            return indicator.hits[0]

        return None

    def _document_to_stix(self, stix):
        return parse(stix.to_dict())
