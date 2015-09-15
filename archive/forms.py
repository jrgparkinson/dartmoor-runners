from django import forms
from easy_select2.widgets import Select2
from .models import Event, Course


class ReimportForm(forms.Form):

    #event = forms.CharField(label='Your name', max_length=100)
    event = forms.ModelChoiceField(queryset=Event.objects.all(), widget=Select2(), label="Choose an event")
    delete_past_results = forms.BooleanField(required=False, label="Delete past results?")


class MoveCourseForm(forms.Form):

    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=Select2(), label="Choose a course to move")
    event = forms.ModelChoiceField(queryset=Event.objects.all(), widget=Select2(), label="Event to move course to")