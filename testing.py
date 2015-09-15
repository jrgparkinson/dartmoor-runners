import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dartmoorrunners.settings")
# Uncomment below for Django 1.7 +
import django

django.setup()

from django.db.models import Q
from archive.models import Runner, Result, Event


#Test that all results are associated with valid runners
for result in Result.objects.all():
    if not result.runner:
        print('Result %s has no runner' % result)

print('***All results tested***')

#Test that all events have organisers
for event in Event.objects.all():
    organisers = event.organisers.all()
    for org in organisers:
        if not org.firstname:
            print('Event %s (%s) has dodgy organisers' % (event, event.notes))

print('***All events tested***')