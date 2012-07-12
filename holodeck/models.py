import uuid

from django.db import models
from holodeck.utils import sample_to_shard_mapper


class Project(models.Model):
    title = models.CharField(max_length=255)
    dashboards = models.ManyToManyField(
        'holodeck.Dashboard',
        blank=True,
        null=True
    )
    api_key = models.CharField(max_length=32, unique=True, blank=True, null=True)

    @classmethod
    def generate_api_key(cls):
        return uuid.uuid4().hex

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = Project.generate_api_key()
        super(Project, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class Dashboard(models.Model):
    title = models.CharField(max_length=255)
    widgets = models.ManyToManyField(
        'holodeck.Widget',
        blank=True,
        null=True
    )
    
    def __unicode__(self):
        return self.title


class Widget(models.Model):
    title = models.CharField(max_length=255)


class LineChartWidget(Widget):
    metrics = models.ManyToManyField(
        'holodeck.Metric',
        blank=True,
        null=True
    )


class Metric(models.Model):
    title = models.CharField(max_length=255)
    project = models.ForeignKey('holodeck.Project')
    sample_interval = models.IntegerField(
        choices=((1, "Every Minute"),)
    )


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
