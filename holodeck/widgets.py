import json
import time

from django.template.loader import render_to_string


class Widget(object):    
    def get_context(self, metric):
        return NotImplementedError

    def render(self, metric):
        context = self.get_context(metric)
        return render_to_string(self.template_name, context)

class LineChart(Widget):
    name = 'Line Chart'
    template_name = 'holodeck/widgets/line_chart.html'

    def get_context(self, metric):
        groups = [group['string_value'] for group in metric.sample_set.all().values('string_value').distinct()]
        [{'string_value': u'random'}, {'string_value': u'series1'}, {'string_value': u'series2'}, {'string_value': u'series3'}]
       
        grouped_samples = []
        group_maxes = []
        sample_count = 50
        for group in groups:
            samples = [(int(time.mktime(sample.timestamp.timetuple()) * 1000), sample.integer_value) for sample in metric.sample_set.filter(string_value=group).order_by('-timestamp')[:sample_count]]
            grouped_samples.append((group, samples))
            group_maxes.append(max([sample[1] for sample in samples]))
        samples = json.dumps([group[1] for group in grouped_samples])

        return {
            'metric': metric,
            'samples': samples,
            'y_max': max(group_maxes) * 1.025,
        }

class PieChart(Widget):
    name = 'Pie Chart'
