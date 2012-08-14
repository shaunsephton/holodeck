import json
import time

from django.template.loader import render_to_string


class Widget(object):
    def get_context(self, metric):
        return NotImplementedError

    def get_groups(self, metric):
        return [group['string_value'] for group in
                metric.sample_set.all().values('string_value').distinct()]

    def render(self, metric):
        context = self.get_context(metric)
        return render_to_string(self.template_name, context)

    def render_export(self, metric):
        pass


class LineChart(Widget):
    name = 'Line Chart'
    template_name = 'holodeck/widgets/line_chart.html'

    def get_context(self, metric):
        context = {
            'metric': metric,
            'width': '600px'
        }

        groups = self.get_groups(metric)

        if not groups:
            context['no_samples'] = True
            return context

        grouped_samples = []
        group_maxes = []
        sample_count = 20
        for group in groups:
            samples = [(int(time.mktime(sample.timestamp.timetuple()) * 1000),
                        sample.integer_value)
                       for sample in metric.sample_set.filter(
                           string_value=group
                       ).order_by('-timestamp')[:sample_count]]
            grouped_samples.append((group, samples))
            group_maxes.append(max([sample[1] for sample in samples]))
        samples = json.dumps([{'label': group[0], 'data': group[1]}
                              for group in grouped_samples])

        context.update({
            'samples': samples,
            'y_max': max(group_maxes) * 1.025,
        })
        return context


class PieChart(Widget):
    name = 'Pie Chart'
    template_name = 'holodeck/widgets/pie_chart.html'

    def get_context(self, metric):
        context = {
            'metric': metric,
            'width': '300px'
        }

        groups = self.get_groups(metric)

        if not groups:
            context['no_samples'] = True
            return context

        grouped_samples = []
        for group in groups:
            sample = metric.sample_set.filter(
                string_value=group).order_by('-timestamp')[0]
            samples = [(0, sample.integer_value)]
            grouped_samples.append((group, samples))
        samples = json.dumps([{'label': group[0], 'data': group[1]}
                             for group in grouped_samples])

        context.update({
            'samples': samples,
        })

        return context


class SampleDeviation(Widget):
    name = 'Sample Deviation'
    template_name = 'holodeck/widgets/sample_deviation.html'

    def calc_deviation(self, primary, secondary):
        if secondary == 0:
            return primary * 100
        return int((primary * 100.0) / secondary) - 100

    def gen_deviation(self, primary, secondary):
        dev = self.calc_deviation(primary, secondary)
        color = 'green'
        if dev >= -10 and dev <= 10:
            color = 'orange'
        if dev < -10:
            color = 'red'
        return {
            'percentage': '%s%s' % ('+' if dev > 0 else '', dev),
            'color': color
        }

    def get_context(self, metric):
        from django.db.models import Avg, Max
        context = {
            'metric': metric,
            'width': '300px'
        }

        try:
            current = metric.sample_set.all().order_by(
                '-timestamp')[0].integer_value
        except IndexError:
            context['no_samples'] = True
            return context
        previous = metric.sample_set.all().order_by(
            '-timestamp')[1].integer_value
        average = int(metric.sample_set.all().aggregate(
            Avg('integer_value'))['integer_value__avg'])
        peak = int(metric.sample_set.all().aggregate(
            Max('integer_value'))['integer_value__max'])

        context.update({
            'current': current,
            'previous': self.gen_deviation(current, previous),
            'average': self.gen_deviation(current, average),
            'peak': self.gen_deviation(current, peak),
        })

        return context
