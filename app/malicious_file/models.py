from django.db import models
import uuid


class MaliciousFile(models.Model):
    id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=255)
    spec_version = models.CharField(max_length=255)
