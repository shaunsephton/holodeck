from django.db import models


class Sample(models.Model):
    value = models.IntegerField()
