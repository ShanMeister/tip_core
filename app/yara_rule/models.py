from django.db import models
import uuid


class YaraRuleModel(models.Model):
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    rule_content = models.TextField()
    created_date = models.DateTimeField()
    modify_date = models.DateTimeField()

