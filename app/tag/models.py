from django.db import models


# Create your models here.
class Tag(models.Model):
    id = models.TextField(primary_key=True)
    tag = models.TextField(max_length=255)
    category = models.TextField(max_length=100)
    created_date = models.DateTimeField()
    modify_date = models.DateTimeField()
