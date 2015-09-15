import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dartmoorrunners.settings")
# Uncomment below for Django 1.7 +
import django
django.setup()

from django.db.models import Q
from archive.models import Runner, Result, Event

# for runner_one in Runner.objects.all():
#
#     for runner_two in Runner.objects.filter(~Q(id=runner_one.id)):
#         if runner_one.firstname == runner_two.firstname and runner_one.surname == runner_two.surname\
#                 and not runner_one == runner_two:
#             print("%s, %s" % (runner_one, runner_two))
#
#
#             # Each runner can have results and events organised, need to remove all references to runner two and then delete them
#             results = Result.objects.filter(runner = runner_two)
#             events = runner_two.event_set.all()
#
#             for result in results:
#                 result.runner = runner_one
#                 result.save()
#                 #pass
#
#             for event in events:
#                 #pass
#                 event.organisers.add(runner_one)
#                 event.organisers.remove(runner_two)
#                 event.save()


# Remove runners with no results or events
for runner in Runner.objects.all():

    #Runners can have: results, events

    results = Result.objects.filter(runner = runner)
    events = runner.event_set.all()

    if not results and not events:
        print(runner)
        #runner.delete()