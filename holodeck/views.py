from django.shortcuts import render_to_response
from django.template import RequestContext


def dashboard(request):
    return render_to_response('holodeck/dashboard.html', {}, context_instance=RequestContext(request))
