from datetime import datetime

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from member.models import Member
from tag.models import Tag
from yara_rule.models import YaraRuleModel


@registry.register_document
class YaraRuleModelDocument(Document):
    author = fields.ObjectField(
        properties={
            "id": fields.KeywordField(),
            "name": fields.KeywordField(),
            "email": fields.KeywordField()
        }
    )

    tag = fields.ObjectField(
        properties={
            "id": fields.KeywordField(),
            "tag": fields.KeywordField(),
            "category": fields.KeywordField()
        }
    )

    id = fields.KeywordField()
    name = fields.KeywordField()


    class Index:
        # Name of the Elasticsearch index
        name = 'cht_tip_yara-rule'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = YaraRuleModel

        fields = [
            'rule_content',
            'created_date',
            'modify_date',
        ]
        related_models = [Member, Tag]

    def get_queryset(self):
        return super().get_queryset().select_related("author")

    def save(self, **kwargs):
        self.created_time = datetime.now()
        self.modify_date = datetime.now()
        return super().save(**kwargs)
