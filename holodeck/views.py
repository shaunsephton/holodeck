from datetime import date
from StringIO import StringIO

from django.contrib import messages
from django.contrib.auth import logout as logout_
from django.contrib.auth import login as login_
from django.contrib.auth.forms import AuthenticationForm
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_protect
from holodeck.models import Dashboard, Metric
from holodeck.decorators import login_required, validate_share
import xlwt


@login_required
def holodeck(request):
    context = {
        'dashboard_list': Dashboard.objects.all().order_by('name')
    }
    return render_to_response(
        'holodeck/dashboard.html',
        context,
        context_instance=RequestContext(request)
    )


@csrf_protect
def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        login_(request, form.get_user())
        return HttpResponseRedirect(
            request.POST.get('next') or reverse('holodeck')
        )
    else:
        request.session.set_test_cookie()

    context = csrf(request)
    context.update({
        'form': form,
    })
    return render_to_response(
        'holodeck/login.html',
        context,
        context_instance=RequestContext(request)
    )


def logout(request):
    logout_(request)
    return HttpResponseRedirect(reverse('holodeck'))


@csrf_protect
@login_required
def manage_dashboard(request, dashboard_id):
    from holodeck.forms import ManageDashboardForm
    dashboard = Dashboard.objects.get(id=dashboard_id)

    form_cls = ManageDashboardForm

    form = form_cls(request.POST or None, instance=dashboard)
    if form.is_valid():
        dashboard = form.save()
        return HttpResponseRedirect(request.path + '?success=1')

    context = {
        'dashboard': dashboard,
        'form': form,
    }
    return render_to_response(
        'holodeck/dashboard/manage.html',
        context,
        context_instance=RequestContext(request)
    )


@csrf_protect
@login_required
def new_dashboard(request):
    from holodeck.forms import NewDashboardForm

    form_cls = NewDashboardForm
    initial = {'owner': request.user.pk}

    form = form_cls(request.POST or None, initial=initial)
    if form.is_valid():
        dashboard = form.save()
        return HttpResponseRedirect(
            reverse('holodeck-view-dashboard', args=[dashboard.pk])
        )

    context = csrf(request)
    context.update({
        'form': form,
    })

    return render_to_response(
        'holodeck/dashboard/new.html',
        context,
        context_instance=RequestContext(request)
    )


def _export_dashboard(request, dashboard_id):
    """
    Exports dashboard as multi-sheet Excel workbook.

    This is a helper method for export_dashboard and export_shared_dashboard
    below. Renders an export without requiring login, should not be exposed
    directly via a URL pattern.
    """
    dashboard = Dashboard.objects.get(id=dashboard_id)

    stream = StringIO()
    workbook = xlwt.Workbook()

    for metric in dashboard.metric_set.all():
        metric.export(workbook)

    workbook.save(stream)

    response = HttpResponse(
        stream.getvalue(),
        mimetype='application/vnd.ms-excel'
    )
    response['Content-Disposition'] = 'attachment; filename="%s-%s.xls"' \
        % (slugify(dashboard.name), date.today())
    stream.close()
    return response


def _view_dashboard(request, dashboard_id, template):
    """
    This is a helper method for view_dashboard and share_dashboard below.
    Renders a dashboard without requiring login, should not be exposed directly
    via a URL pattern.
    """
    dashboard = Dashboard.objects.get(id=dashboard_id)
    context = {
        'dashboard': dashboard,
        'metrics': dashboard.metric_set.all()
    }
    return render_to_response(
        template,
        context,
        context_instance=RequestContext(request)
    )


@login_required
def export_dashboard(request, dashboard_id):
    return _export_dashboard(request, dashboard_id)


@validate_share
def export_shared_dashboard(request, dashboard_id, share_key):
    return _export_dashboard(request, dashboard_id)


@login_required
def remove_dashboard(request, dashboard_id):
    dashboard = Dashboard.objects.get(id=dashboard_id)
    dashboard.delete()
    return HttpResponseRedirect(
        reverse('holodeck')
    )


@validate_share
def share_dashboard(request, dashboard_id, share_key):
    return _view_dashboard(
        request,
        dashboard_id,
        'holodeck/dashboard/share.html'
    )

@login_required
def sort_dashboard(request, dashboard_id):
    for position, id in enumerate(request.GET['order'].split(',')):
        metric = Metric.objects.get(id=id.split('_')[-1])
        metric.position = position
        metric.save()
    return HttpResponse('success')


@login_required
def view_dashboard(request, dashboard_id):
    return _view_dashboard(
        request,
        dashboard_id,
        'holodeck/dashboard/view.html'
    )


@csrf_protect
@login_required
def new_metric(request, dashboard_id):
    from holodeck.forms import NewMetricForm
    dashboard = Dashboard.objects.get(id=dashboard_id)

    form_cls = NewMetricForm
    initial = {}

    form = form_cls(request.POST or None, initial=initial)
    if form.is_valid():
        metric = form.save(commit=False)
        metric.dashboard = dashboard
        metric.save()

        return HttpResponseRedirect(
            reverse('holodeck-manage-metric', args=[metric.pk])
        )

    context = csrf(request)
    context.update({
        'form': form,
        'dashboard': dashboard,
    })

    return render_to_response(
        'holodeck/metric/new.html',
        context,
        context_instance=RequestContext(request)
    )


@csrf_protect
@login_required
def manage_metric(request, metric_id):
    from holodeck.forms import ManageMetricForm
    metric = Metric.objects.get(id=metric_id)
    dashboard = metric.dashboard

    form_cls = ManageMetricForm

    form = form_cls(request.POST or None, instance=metric)
    if form.is_valid():
        metric = form.save()
        return HttpResponseRedirect(request.path + '?success=1')

    context = {
        'dashboard': dashboard,
        'metric': metric,
        'form': form,
    }
    return render_to_response(
        'holodeck/metric/manage.html',
        context,
        context_instance=RequestContext(request)
    )


@login_required
def remove_metric(request, metric_id):
    metric = Metric.objects.get(id=metric_id)
    dashboard = metric.dashboard
    metric.delete()
    return HttpResponseRedirect(
        reverse('holodeck-view-dashboard', args=[dashboard.pk])
    )


@login_required
def purge_metric_samples(request, metric_id):
    # TODO: Needs a warning.
    metric = Metric.objects.get(id=metric_id)
    metric.sample_set.all().delete()
    messages.success(
        request,
        'All samples for this metric have been purged/removed.'
    )
    return HttpResponseRedirect(
        reverse('holodeck-manage-metric', args=[metric.id])
    )
