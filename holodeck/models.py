import uuid

from django.contrib.auth.models import User
from django.db import models
from holodeck.utils import get_widget_type_choices, load_class_by_string


class Dashboard(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.name


class Metric(models.Model):
    name = models.CharField(max_length=255)
    dashboard = models.ForeignKey('holodeck.Dashboard')
    widget_type = models.CharField(
        max_length=64,
        choices=get_widget_type_choices()
    )
    api_key = models.CharField(
        max_length=32,
        unique=True,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.name

    @classmethod
    def generate_api_key(cls):
        return uuid.uuid4().hex

    def render(self):
        return load_class_by_string(self.widget_type)().render(self)

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = Metric.generate_api_key()
        super(Metric, self).save(*args, **kwargs)


class Sample(models.Model):
    metric = models.ForeignKey('holodeck.Metric')
    integer_value = models.IntegerField()
    string_value = models.CharField(max_length=64)
    timestamp = models.DateTimeField()
