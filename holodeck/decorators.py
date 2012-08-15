from functools import wraps

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from holodeck.models import Dashboard

def login_required(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated():
            request.session['_next'] = request.build_absolute_uri()
            return HttpResponseRedirect(reverse('holodeck-login'))
        return func(request, *args, **kwargs)
    return wrapped

def validate_share(func):
    @wraps(func)
    def wrapped(request, dashboard_id, share_key, *args, **kwargs):
        try:
            Dashboard.objects.get(id=dashboard_id, share_key=share_key)
        except Dashboard.DoesNotExist:
            raise Http404
        return func(request, dashboard_id, share_key, *args, **kwargs)
    return wrapped
