from django import template
from holodeck.models import Dashboard

register = template.Library()


@register.inclusion_tag('holodeck/inclusion_tags/dashboard_dropdown.html', takes_context=True)
def dashboard_dropdown(context):
    context.update({
        'dashboard_list': Dashboard.objects.all().order_by('name')
    })
    return context
