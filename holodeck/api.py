import base64
from datetime import datetime
import json

from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from holodeck.models import Metric, Sample


@csrf_exempt
def store(request):
    """
    Main API method storing pushed data.
    TODO: Needs a lot of work, security, validation etc.
    """
    if request.method == 'POST':
        data = request.raw_post_data
        data = json.loads(base64.b64decode(data).decode('zlib'))

        # Get the Metric from provided ID, otherwise fail with NotFound.
        try:
            metric = Metric.objects.get(id=int(data['metric_id']))
        except Metric.DoesNotExist:
            return HttpResponseNotFound()

        # Validate api_key, otherwise fail with Forbidden.
        if metric.api_key != data['api_key']:
            return HttpResponseForbidden()

        timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')

        for sample in data['samples']:
            # TODO: get_or_create or check uniqueness on subset of fields?
            Sample.objects.create(metric_id=metric.pk, string_value=sample[0], integer_value=sample[1], timestamp=timestamp)

    return HttpResponse()
