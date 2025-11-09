from django.db import models


class Member(models.Model):
    id = models.TextField(primary_key=True)
    email = models.TextField(max_length=320)
    name = models.TextField(max_length=100)
    created_date = models.DateTimeField()
    modify_date = models.DateTimeField()
