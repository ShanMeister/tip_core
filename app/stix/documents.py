from datetime import datetime

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from stix.models import StixDomainObject, StixMetaObject


@registry.register_document
class StixDomainObjectDocument(Document):
    id = fields.KeywordField()
    type = fields.KeywordField()
    specVersion = fields.KeywordField()
    created_by_ref = fields.KeywordField()
    labels = fields.ObjectField()
    confidence = fields.IntegerField()
    lang = fields.KeywordField()
    external_references = fields.ObjectField()
    object_marking_refs = fields.ObjectField()
    granular_markings = fields.ObjectField()
    extensions = fields.ObjectField()

    class Index:
        name = 'stix_domain_object'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = StixDomainObject
        fields = [
            'created',
            'modified'
        ]


@registry.register_document
class StixMetaObjectDocument(Document):
    id = fields.KeywordField()
    type = fields.KeywordField()
    specVersion = fields.KeywordField()
    created_by_ref = fields.KeywordField()

    class Index:
        name = 'stix_meta_object'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = StixMetaObject
        fields = [
            'created',
            'modified'
        ]

