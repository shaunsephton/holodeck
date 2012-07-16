from django import forms
from django.utils.translation import ugettext_lazy as _
from holodeck.models import Dashboard, Metric


class NewDashboardForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': _('e.g. My Dashboard Name')}))

    class Meta:
        fields = ('name', 'owner')
        model = Dashboard


class NewMetricForm(forms.ModelForm):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': _('e.g. My Metric Name')}))

    class Meta:
        fields = ('name', 'widget_type', )
        model = Metric


class ManageMetricForm(NewMetricForm):
    class Meta:
        fields = ('name', 'dashboard', 'widget_type', )
        model = Metric
