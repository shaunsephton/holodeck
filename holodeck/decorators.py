from functools import wraps

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def login_required(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        if not settings.PUBLIC:
            if not request.user.is_authenticated():
                request.session['_next'] = request.build_absolute_uri()
                return HttpResponseRedirect(reverse('holodeck-login'))
        return func(request, *args, **kwargs)
    return wrapped
