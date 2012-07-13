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
    samples = metric.sample_set.all().order_by('-timestamp')
    return {
        'metric': metric,
        'samples': samples
    }
