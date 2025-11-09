from datetime import datetime

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from member.models import Member
from tag.models import Tag


@registry.register_document
class TagDocument(Document):
    id = fields.KeywordField()
    author = fields.ObjectField(
        properties={
            "id": fields.KeywordField(),
            "name": fields.KeywordField(),
            "email": fields.KeywordField()
        }
    )

    tag = fields.KeywordField()
    category = fields.KeywordField()

    class Index:
        name = 'cht_tip_tag'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Tag

        fields = [
            'created_date',
            'modify_date'
        ]
        related_models = [Member]

    def save(self, **kwargs):
        self.modify_date = datetime.now()
        return super().save(**kwargs)
