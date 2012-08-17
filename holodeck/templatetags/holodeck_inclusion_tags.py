from copy import copy

from django import template
from holodeck.models import Dashboard
from holodeck.widgets import LineChart, SampleDeviation

register = template.Library()


@register.inclusion_tag('holodeck/inclusion_tags/dashboard_dropdown.html', takes_context=True)
def dashboard_dropdown(context):
    context.update({
        'dashboard_list': Dashboard.objects.all().order_by('name')
    })
    return context


@register.inclusion_tag('holodeck/inclusion_tags/render_metric.html', takes_context=True)
def render_metric(context, metric):
    context = copy(context)
    return {'result': metric.render(context)}


@register.inclusion_tag('holodeck/inclusion_tags/dashboard_list_summary.html')
def dashboard_list_summary(dashboard):
    context = {
        'dashboard': dashboard,
    }

    metrics = dashboard.metric_set.filter(
        widget_type='holodeck.widgets.LineChart'
    )

    sampled_metric = None
    for metric in metrics:
        if metric.sample_set.all():
            sampled_metric = metric
            break

    if not sampled_metric:
        return context

    chart_context = LineChart().get_context(sampled_metric)
    # TODO: Calculate this here, unused context calculated.
    deviation_context = SampleDeviation().get_context(sampled_metric)

    return {
        'metric': sampled_metric,
        'dashboard': dashboard,
        'samples': chart_context['samples'],
        'y_max': chart_context['y_max'] * 1.5,
        'previous': deviation_context['previous']
    }
