from django.db import models


# Create your models here.
class StixDomainObject(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField(max_length=50)
    specVersion = models.TextField(max_length=100)
    created_by_ref = models.TextField(max_length=100)
    labels = models.TextField(max_length=255)
    confidence = models.IntegerField()
    lang = models.TextField(max_length=50)
    external_references = models.TextField(max_length=255)
    object_marking_refs = models.TextField(max_length=255)
    granular_markings = models.TextField(max_length=255)
    extensions = models.TextField(max_length=255)

    created = models.DateTimeField()
    modified = models.DateTimeField()


class StixMetaObject(models.Model):
    id = models.TextField(primary_key=True)
    type = models.TextField(max_length=50)
    specVersion = models.TextField(max_length=100)
    created_by_ref = models.TextField(max_length=100)

    created = models.DateTimeField()
    modified = models.DateTimeField()