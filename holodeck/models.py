from django.db import models
from holodeck.utils import sample_to_shard_mapper


class Project(models.Model):
    title = models.CharField(max_length=255)
    dashboards = models.ManyToManyField(
        'holodeck.Dashboard',
        blank=True,
        null=True
    )

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
    sample_interval = models.IntegerField(
        choices=((1, "Every Minute"),)
    )


class GoogleAnalyticsUniqueUserMetric(Metric):
    access_token = models.CharField(max_length=64)


class Sample(models.Model):
    metric_id = models.IntegerField(max_length=64)
    integer = models.IntegerField()
    string = models.CharField(max_length=64)

    def save(self, *args, **kwargs):
        self.full_clean()
        kwargs.update({'using': 'shard_%s' % sample_to_shard_mapper(self)})
        super(Sample, self).save(*args, **kwargs)
