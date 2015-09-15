
import heapq
import re
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import RequestContext, loader
from os import listdir
from os.path import isfile, join
import math
from .import_data import import_table, parse_webpage_for_event, parse_google_sheet, parse_docx_file
from .models import Event, Result, Runner, Series, Course, Alias
from .forms import ReimportForm, MoveCourseForm
import numpy as np

# Create your views here.
def index(request):
    events_list = Event.objects.order_by('-date')

    raw_series_list = Series.objects.order_by('-year')
    series_list = []

    # Make sure the series have events attached to them
    for series in raw_series_list:
        events_for_series = Event.objects.filter(series = series)
        if events_for_series:
            series_list.append(series)

    # Get statistics
    stats = {}
    stats['num_events'] = Event.objects.filter(number_increment = 1).count()
    stats['num_results'] = Result.objects.all().count()
    stats['num_runners'] = Runner.objects.all().count()
    stats['num_series'] = Series.objects.all().count()
    stats['num_winter_series'] = Series.objects.filter(season = Series.WINTER).count()
    stats['num_summer_series'] = Series.objects.filter(season = Series.SUMMER).count()

    template = loader.get_template('archive/index.html')
    context = RequestContext(request, {
        'events_list': events_list,
        'series_list': series_list,
        'stats': stats,
    })
    return HttpResponse(template.render(context))


def event(request, event_id):
    this_event = get_object_or_404(Event, pk=event_id)
    results = Result.objects.filter(event__id = event_id).order_by('position')
    organisers = this_event.organisers.all()
    courses = Course.objects.filter(event__id = event_id)


    # We need to deal with the situation where an event consists of more than one time/score,
    # by collating results for the same runner

    results_list = Result.collate_result_set(results)

    #Create the column headings
    result_types = []
    if results_list:
        for result in results_list[0]:
            result_types.append(result.type)

    template = loader.get_template('archive/event.html')
    context = RequestContext(request, {
        'results_list': results_list,
        'result_types': result_types,
        'event': this_event,
        'organisers': organisers,
        'courses': courses,
    })


    return HttpResponse(template.render(context))


def runner(request, runner_id):
    this_runner = get_object_or_404(Runner, pk = runner_id)

    results = Result.objects.filter(runner__id = runner_id)
    results_list = []

    for result in results:
        event = Event.objects.get(pk=result.event_id)
        if event:
            result_string = "<a href='/archive/event/%s'>" + str(event.date) + " - " + event.location + "</a> - " + result.get_formatted_time()
            results_list.append(result_string % event.id)

    events = this_runner.event_set.all()

    template = loader.get_template('archive/runner.html')
    context = RequestContext(request, {
        'results': results_list,
        'events': events,
        'runner': this_runner
    })


    return HttpResponse(template.render(context))

def series(request, series_id):
    series = get_object_or_404(Series, pk = series_id)
    events = Event.objects.filter(series = series).order_by('-date')

    template = loader.get_template('archive/series.html')
    context = RequestContext(request, {
        'events': events,
        'series': series,
    })

    return HttpResponse(template.render(context))


def missing_data(request):

    events_no_results = []
    events_no_location = []
    events_no_organisers = []
    events_few_results = []

    UNKNOWN_ORGANISER = Runner.objects.filter(firstname = 'Planner', surname='Unknown')[0]

    for event in Event.objects.all():
        # Events without results
        results = Result.objects.filter(event__id=event.id)
        if not results:
            events_no_results.append(event)
        elif len(results) < 5:
            events_few_results.append(event)


        # Events without location
        if not event.location or event.location == "?":
            events_no_location.append(event)

        # Events without organisers
        organisers = event.organisers.all()
        if not organisers or organisers[0] == UNKNOWN_ORGANISER:
            events_no_organisers.append(event)


    # Series without events?


    template = loader.get_template('archive/missing_data.html')
    context = RequestContext(request, {
        'events_no_results': events_no_results,
        'events_no_location': events_no_location,
        'events_no_organisers': events_no_organisers,
        'events_few_results': events_few_results,
    })

    return HttpResponse(template.render(context))

def series_list(request):
    winter_series = Series.objects.filter(season = Series.WINTER)
    summer_series = Series.objects.filter(season = Series.SUMMER)

    template = loader.get_template('archive/series_list.html')
    context = RequestContext(request, {
        'summer_series': summer_series,
        'winter_series': winter_series,
    })

    return HttpResponse(template.render(context))

def events_list(request):
    events = Event.objects.all()

    template = loader.get_template('archive/events_list.html')
    context = RequestContext(request, {
        'events': events,
    })

    return HttpResponse(template.render(context))

def runners_list(request):
    runners = Runner.objects.all()

    num_columns = 4
    column_length = math.ceil(len(runners)/num_columns)

    template = loader.get_template('archive/runners_list.html')
    context = RequestContext(request, {
        'runners': runners,
        'column_length': column_length,
    })

    return HttpResponse(template.render(context))

def tools(request):
    message = ""

    reimport_form = ReimportForm()
    move_course_form = MoveCourseForm()

    template = loader.get_template('archive/tools.html')
    context = RequestContext(request, {
        'message': message,
        'reimport_form': reimport_form,
        'move_course_form': move_course_form,
    })

    return HttpResponse(template.render(context))

def merge_duplicate_runners(request):

    success_message = None
    failed_message = None

    for runner_one in Runner.objects.all():

        runners_to_merge = []

        # Find identically named runners
        for runner_two in Runner.objects.filter(~Q(id=runner_one.id)):
            if runner_one.firstname == runner_two.firstname and runner_one.surname == runner_two.surname\
                    and not runner_one == runner_two:
                print("%s, %s" % (runner_one, runner_two))
                runners_to_merge.append(runner_two)

        #Find alias runners
        aliases = Alias.objects.filter(runner = runner_one)
        for alias in aliases:
            alias_runners = Runner.objects.filter(firstname=alias.firstname, surname=alias.surname)
            for alias_runner in alias_runners:
                runners_to_merge.append(alias_runner)

        for runner_two in runners_to_merge:

            #Just double check we're not trying to merge the same runner. This would be bad.
            if runner_two == runner_one:
                continue

            # Each runner can have results and events organised, need to remove all references to runner two and then delete them
            results = Result.objects.filter(runner = runner_two)
            events = runner_two.event_set.all()

            for result in results:
                result.runner = runner_one
                result.save()
                #pass

            for event in events:
                #pass
                event.organisers.add(runner_one)
                event.organisers.remove(runner_two)
                event.save()


    # Remove runners with no results or events
    for runner in Runner.objects.all():

        #Runners can have: results, events

        results = Result.objects.filter(runner = runner)
        events = runner.event_set.all()

        if not results and not events:
            #print(runner)
            runner.delete()

    success_message = "Successfully merged duplicate runners"

    template = loader.get_template('archive/tools/tool_response.html')
    context = RequestContext(request, {
        'success_message': success_message,
        'failed_message': failed_message,
    })

    return HttpResponse(template.render(context))


def reimport(request):
    success_message = None
    failed_message = None


    if request.method == 'POST':
        # create a form instance and populate it with data from the request:


        event_id = request.POST['event']
        event = Event.objects.get(pk = event_id)


        if not event:
            failed_message = "No event selected"
        else:
            rows = None
            first_result_row = -1

            #Determine source type and get the table
            if event.source.find('dropbox') > -1:
                dir = 'C:\\Users\\Jamie\\Dropbox\\DR Run results copy\\docx_converted\\'
                docx_files = [ f for f in listdir(dir) if isfile(join(dir,f)) ]

                regexp = re.compile(r'https:\/\/www\.dropbox\.com\/sh\/[a-z0-9]+\/[^\/]+\/(\d{3}%20\d{2}-\d{2}-\d{2}(%20w\d)?\.docx)\?dl=0')
                m = re.match(regexp, str(event.source))
                if m:
                    filename = m.group(1).replace('%20',' ')

                    result_file = None
                    print(docx_files)
                    for f in docx_files:
                        if f.find(filename) > -1 and f.find('old') == -1:
                            result_file = filename

                    if not result_file:
                        failed_message =  "Couldn't find the docx file"

                    if request.POST['delete_past_results']:
                        event.delete_past_results()

                    (rows, first_result_row) = parse_docx_file(result_file, dir, event)

                else:
                    failed_message = "Couldn't handle the source file url"

            elif  event.source.find('docs.google.com/spreadsheets') > -1:
                # Google docs
                (rows, first_result_row) = parse_google_sheet(event.source, event)

            elif event.source.find('dartmoorrunners.co.uk') > -1:
                #Web page table
                (rows, first_result_row) = parse_webpage_for_event(event.source, event)

            else:
               failed_message = "Don't know how to deal with this event"

            if rows:

                if request.POST['delete_past_results']:
                    event.delete_past_results()

                success = import_table(rows, event, first_result_row)

                if success:
                    success_message = "Succesfully imported event %s" % event
                else:
                    failed_message = "Unable to import the table"

            else:
                failed_message = "Couldn't parse the table"


    else:
        failed_message = "No event selected"


    template = loader.get_template('archive/tools/tool_response.html')
    context = RequestContext(request, {
        'success_message': success_message,
        'failed_message': failed_message
    })

    return HttpResponse(template.render(context))


def move_course(request):
    failed_message = None
    success_message = None

    if request.method == 'POST':
        event_id = request.POST['event']
        course_id = request.POST['course']

        event = Event.objects.get(pk = event_id)
        course = Course.objects.get(pk = course_id)

        if not event or not course:
            failed_message = "Couldn't find the event or course selected"

        else:
            #Move the course
            course.event = event
            course.save()

            #Move the results associated with the course
            results = Result.objects.filter(course_id = course.id)
            for res in results:
                res.event = event
                res.save()

            success_message = "Course and results moved to %s" % event

    else:
        failed_message = "No form submitted"

    template = loader.get_template('archive/tools/tool_response.html')
    context = RequestContext(request, {
        'success_message': success_message,
        'failed_message': failed_message
    })

    return HttpResponse(template.render(context))


#Find and remove results that don't have a course but are part of an event with courses, and therefore don't show up
def remove_ghost_results(request):

    success_message = None
    failed_message = None
    count = 0

    for event in Event.objects.all():
        courses = Course.objects.filter(event_id = event.id)
        if len(courses) == 0:
            continue

        #This event has courses, find it's results and check they're assigned to a course
        results = Result.objects.filter(event_id = event.id)
        for res in results:
            if not res.course_id:
                res.delete()
                count = count + 1

    if count > 0:
        success_message = "%d ghost results removed" % count
    else:
        success_message = "No ghost results found"

    template = loader.get_template('archive/tools/tool_response.html')
    context = RequestContext(request, {
        'success_message': success_message,
        'failed_message': failed_message
    })

    return HttpResponse(template.render(context))

def overall_results(request, series_id):
    series = Series.objects.get(pk = series_id)
    events = Event.objects.filter(series_id = series_id).order_by('date')

    results_for_event = {}
    series_runners = []
    series_results = []
    #Structure of series_results:
    # [ [runner 1, points in event 1, points in event 2 ....],
    #   [runner 2, points in event 1, points in event 2 ....] ]

    # First find all the runners who competed in this series
    for event in events:
        results = Result.objects.filter(event_id = event.id)
        results_for_event[event] = results
        for result in results:
            runner = result.runner
            if not runner in series_runners:
                series_runners.append(runner)


    # Go through each runner and get their points from each event
    for runner in series_runners:
        series_result = [runner]
        for event in events:
            result = Result.objects.filter(event_id = event.id, runner_id = runner.id)
            if result:
                series_result.append(result[0].points)
            else:
                series_result.append('')

        series_results.append(series_result)

    # Calculate organisers points - average of best up to 3 events (0 if no events)
    i = 1
    for event in events:
        for organiser in event.organisers.all():
            if organiser in series_runners:
                #Find the results for this runner
                for series_result in series_results:
                    if series_result[0] == organiser:
                        #Find three best current results and average them
                        results = series_result[1:]

                        #Remove blank strings
                        numeric = []
                        for res in results:
                            if res != '':
                                numeric.append(res)

                        top_three = heapq.nlargest(3, numeric)
                        average = np.mean(top_three)

                        series_result[i] = average


            else:
                #If you haven't had any other runs, you don't get anything for the event you organised
                pass
        i = i+1

    # Calculate overall results - sum top 3 results
    for series_result in series_results:
        results = series_result[1:]

        #Remove blank strings
        numeric = []
        for res in results:
            if res != '':
                numeric.append(res)

        top_three = heapq.nlargest(3, numeric)
        sum = np.sum(top_three)
        series_result.append(sum)

    # Sort the table by the overall points column
    overall_column = len(series_results[0]) - 1
    series_results = sorted(series_results,key=lambda l:l[overall_column], reverse=True)

    #Format all points correctly
    for i in range(len(series_results)):
        series_result = series_results[i]
        for j in range(1, len(series_result)):
            if series_result[j] != '':
                series_result[j] = "%.2f" % series_result[j]

    template = loader.get_template('archive/overall_results.html')
    context = RequestContext(request, {
        'series': series,
        'series_results': series_results,
        'events': events,
    })

    return HttpResponse(template.render(context))


def events_on_map(request):
    #Google API key: AIzaSyCPe79VkpqkyLaCsHiQx3jIBfEZs_J8SYA
    events = []
    for event in Event.objects.all():
        if event.lat and event.lat:
            events.append(event)

    template = loader.get_template('archive/events_on_map.html')
    context = RequestContext(request, {
        'events': events,
    })

    return HttpResponse(template.render(context))