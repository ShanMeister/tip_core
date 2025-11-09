from datetime import datetime

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from member.models import Member


@registry.register_document
class MemberDocument(Document):
    id = fields.TextField()
    class Index:
        name = 'cht_tip_member'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Member

        fields = [
            'email',
            'name',
            'created_date',
            'modify_date'
        ]

    def save(self, **kwargs):
        self.created_time = datetime.now()
        self.modify_date = datetime.now()
        return super().save(**kwargs)
