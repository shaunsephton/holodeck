import json
import time

from django.template.loader import render_to_string


class Widget(object):    
    def get_context(self, metric):
        return NotImplementedError

    def get_groups(self, metric):
        return [group['string_value'] for group in metric.sample_set.all().values('string_value').distinct()]

    def render(self, metric):
        context = self.get_context(metric)
        return render_to_string(self.template_name, context)

class LineChart(Widget):
    name = 'Line Chart'
    template_name = 'holodeck/widgets/line_chart.html'

    def get_context(self, metric):
        groups = self.get_groups(metric)
        grouped_samples = []
        group_maxes = []
        sample_count = 25
        for group in groups:
            samples = [(int(time.mktime(sample.timestamp.timetuple()) * 1000), sample.integer_value) for sample in metric.sample_set.filter(string_value=group).order_by('-timestamp')[:sample_count]]
            grouped_samples.append((group, samples))
            group_maxes.append(max([sample[1] for sample in samples]))
        samples = json.dumps([{'label': group[0], 'data': group[1]} for group in grouped_samples])
        return {
            'metric': metric,
            'samples': samples,
            'y_max': max(group_maxes) * 1.025,
            'width': '600px'
        }

class PieChart(Widget):
    name = 'Pie Chart'
    template_name = 'holodeck/widgets/pie_chart.html'

    def get_context(self, metric):
        groups = self.get_groups(metric)
        grouped_samples = []
        for group in groups:
            sample = metric.sample_set.filter(string_value=group).order_by('-timestamp')[0]
            samples = [(0, sample.integer_value)]
            grouped_samples.append((group, samples))
        samples = json.dumps([{'label': group[0], 'data': group[1]} for group in grouped_samples])

        return {
            'metric': metric,
            'samples': samples,
            'width': '300px'
        }
