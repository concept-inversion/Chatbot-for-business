from django.db import models


class UserQuery(models.Model):
    username = models.CharField(max_length=100)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

