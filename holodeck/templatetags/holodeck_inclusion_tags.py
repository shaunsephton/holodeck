import time

from django import template
from holodeck.models import Dashboard

register = template.Library()


@register.inclusion_tag('holodeck/inclusion_tags/dashboard_dropdown.html')
def dashboard_dropdown():
    return {
        'object_list': Dashboard.objects.all().order_by('name')
    }


@register.inclusion_tag('holodeck/inclusion_tags/render_metric.html')
def render_metric(metric):
    sample_objs = metric.sample_set.all().order_by('-timestamp')

    samples = []
    y_max = 0
    for sample_obj in sample_objs[:40]:
        if sample_obj.integer_value > y_max:
            y_max = sample_obj.integer_value

        samples.append((int(time.mktime(sample_obj.timestamp.timetuple()) * 1000), sample_obj.integer_value))

    y_max += y_max * 0.05

    return {
        'metric': metric,
        'samples': samples,
        'y_max': y_max,
    }
