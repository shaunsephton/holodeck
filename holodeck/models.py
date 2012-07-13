import uuid

from django.db import models
from holodeck.utils import metric_to_shard_mapper, sample_to_shard_mapper
from django.contrib.auth.models import User

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
        choices=(('line_chart', 'Line Chart'),)
    )
    api_key = models.CharField(max_length=32, unique=True, blank=True, null=True)


    @classmethod
    def generate_api_key(cls):
        return uuid.uuid4().hex

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = Metric.generate_api_key()
        super(Metric, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name

    @property
    def sample_set(self):
        return Sample.objects.filter(metric_id=self.id).using('shard_%s' % metric_to_shard_mapper(self))


class GoogleAnalyticsUniqueUserMetric(Metric):
    access_token = models.CharField(max_length=64)


class Sample(models.Model):
    metric_id = models.IntegerField(max_length=64)
    integer_value = models.IntegerField()
    string_value = models.CharField(max_length=64)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.full_clean()
        kwargs.update({'using': 'shard_%s' % sample_to_shard_mapper(self)})
        super(Sample, self).save(*args, **kwargs)
