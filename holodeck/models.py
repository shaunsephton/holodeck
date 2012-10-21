import uuid

from django.contrib.auth.models import User
from django.db import models
from holodeck.utils import get_widget_type_choices, load_class_by_string
import xlwt


def generate_key():
    return uuid.uuid4().hex


class Dashboard(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, null=True)
    share_key = models.CharField(
        max_length=32,
        unique=True,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.share_key:
            self.share_key = generate_key()
        super(Dashboard, self).save(*args, **kwargs)

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
    share_key = models.CharField(
        max_length=32,
        unique=True,
        blank=True,
        null=True
    )
    position = models.IntegerField(
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return self.name
    
    @property
    def widget(self):
        return load_class_by_string(self.widget_type)()

    def render(self, context, minimal=False):
        return self.widget.render(self, context, minimal)

    def export(self, workbook):
        """
        Given a xlwt Excel workbook creates a sheet and populates it
        with samples for this metric.
        """
        samples = {}
        worksheet = workbook.add_sheet(self.name)

        samples = self.sample_set.all()

        date_format = 'D-MMM-YY H:MM:SS'
        date_style = xlwt.easyxf(num_format_str=date_format)

        # Write distinct reverse sorted timestamps as first column.
        timestamps = list(set([sample.timestamp for sample in samples]))
        timestamps.sort(reverse=True)
        for i, timestamp in enumerate(timestamps):
            worksheet.write(i + 1, 0, timestamp, date_style)

        # Set timestamp column width.
        # Each character's approximated width is 256
        worksheet.col(0).width = (1 + len(date_format)) * 256

        # Write distinct sorted string values as first row.
        string_values = list(set([sample.string_value for sample in samples]))
        string_values.sort()
        for i, string_value in enumerate(string_values):
            worksheet.write(0, i + 1, string_value)
            worksheet.col(i + 1).width = (1 + len(string_value)) * 256

        # Write sample values as they correspond to timestamp and string_value.
        for sample in samples:
            row = timestamps.index(sample.timestamp) + 1
            col = string_values.index(sample.string_value) + 1

            try:
                worksheet.write(row, col, sample.integer_value)
                if len(str(sample.integer_value)) > len(sample.string_value):
                    worksheet.col(col).width = (
                        1 + len(str(sample.integer_value))
                    ) * 256
            except Exception, e:
                if 'overwrite' in e.message:
                    # Ignore duplicate samples.
                    # XXX: Enforce on import.
                    pass
                else:
                    raise e

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = generate_key()
        if not self.share_key:
            self.share_key = generate_key()
        super(Metric, self).save(*args, **kwargs)

    class Meta:
        ordering = ['position', '-id']


class Sample(models.Model):
    metric = models.ForeignKey('holodeck.Metric')
    integer_value = models.IntegerField(
        default=0
    )
    string_value = models.CharField(max_length=64)
    timestamp = models.DateTimeField()

    class Meta:
        unique_together = (
            ("metric", "string_value", "timestamp"),
        )
