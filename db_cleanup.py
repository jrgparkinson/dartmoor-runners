from datetime import timedelta
import re
from os.path import isfile, join
import pypyodbc
from spyderlib.widgets.explorer import listdir


__author__ = 'Jamie'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dartmoorrunners.settings")
# Uncomment below for Django 1.7 +
import django
django.setup()


from archive.models import Event, Result, Series, Runner, ResultDataType
from archive.import_data import *


print(os.path)


WEBPAGES = {
    'summer_2011': '',
    'winter_2011': "http://dartmoorrunners.co.uk/results_16.html",
    'summer_2012': "http://dartmoorrunners.co.uk/results_17.html",
    'winter_2012': "https://docs.google.com/spreadsheets/d/1hH16Umc6ZQ7fVtV1OhsRzd8OYWJkxG7MbBZAz9csZUk/pub?output=html",
    'summer_2013': "https://docs.google.com/spreadsheets/d/1FFqZTWWyxT0gsG-DQ5fFbfgCWhg1qw6peKEt1-9Yo94/pub?output=html",
    'winter_2013': "https://docs.google.com/spreadsheet/pub?key=0Ah6BnD-JmyoRdHB1Tk40cFI3UTZXUmpCRUlyd0UzS3c&output=html",
    'summer_2014': "https://docs.google.com/spreadsheets/d/13SWq_Fh1JIONZeoMtpFdRE-JEUYCs6aTskbxPE5D924/pub?output=html",
    'winter_2014': "https://docs.google.com/spreadsheets/d/1goEKF8pbKLPJPcTfi-g0EJVk59VwJ6zXmiZmb3oo8bo/pub?output=html",
    'summer_2015': "https://docs.google.com/spreadsheets/d/1UbpBXZtNpU5sgKH7B_zmTcWf-QdXMJ0tyQB1o9U-Ay0/pub?output=html",
    }

def print_events_with_course_notes():
    for event in Event.objects.all():
        for result in Result.objects.filter(event_id = event.id):
            if result.notes.find("[") > -1:
                print(str(event.id) + ",  " + str(event))
                break


def remove_points_from_notes():

    re_float = re.compile(r'^[0-9]{2,3}\.[0-9]{2}$')
    for event in Event.objects.all():
        #event.calculate_points()
        for res in Result.objects.filter(event_id = event.id):
            if re.match(re_float, res.notes):
                print(str(event))
                #event.remove_points_from_notes()
                break


#Make event number
def make_event_number():
    i = 1
    for event in Event.objects.order_by('date'):
        if event.id > -1:
            event.number = i
            event.save()
            i = i + event.number_increment

    print('Calculated event numbers')

for event in Event.objects.all():
    event.make_lat_lon()


for event in Event.objects.all():
    if event.lat and event.lon:
        print("%s, %s, %s, %s, %s" % (event.location, str(event), event.lat, event.lon, 1))



#Update series field
# for event in Event.objects.all():
#     # First winter series - September 96
#     m = re.match(r'(\d{4})-(\d{2})-\d{2}', str(event.date))
#     year = int(m.group(1))
#     month = int(m.group(2))
#
#     if 9 <= month <= 12:
#         series_season = 'Winter'
#         series_number = (year - 1996) + 1
#
#     elif 1 <= month <= 8:
#         series_season = 'Summer'
#         series_number = (year - 1994) + 1
#
#     else:
#         continue
#
#     series = Series.objects.filter(number = series_number, season = series_season)
#
#     if len(series) > 0:
#         event.series = series[0]
#         event.save()
#
#         series[0].year = year
#         series[0].save()
#     else:
#         print('No series found for %s' % str(event))
#
#
#

# Fix stupidly long (>12hrs) times
# results = Result.objects.all()
# for result in results:
#     if result.time > 12*3600:
#         result.time = result.time - 12*3600
#         print(result.get_formatted_time())
#
#         result.save()





#Get organisers
# events = Event.objects.all()
#
# for event in events:
#     print(event.organisers)
#     old_event = E()
#     old_event.populate_for_id(connection, event.id)
#     event.organisers = old_event.get_organisers_string()
#     event.save()


#Cleanup gridrefs
# events = Event.objects.all()
# for event in events:
#     # location = re.sub(r',\s+SX\s?\d{3}\s?\d{3}\s?$','',event.location)
#     # print(location)
#     # event.location = location
#     gridref = re.sub(r'\s','', event.gridref)
#     print(gridref)
#     event.gridref = gridref
#
#
#     event.save()










#Find grid refs
# events = Event.objects.all()
#
# for event in events:
#     if event.gridref:
#         #print(event.gridref)
#         continue
#
#     m = re.findall(r'(SX\s+\d{3}\s+\d{3})', event.location + event.notes)
#     if len(m) > 0:
#         new_grid_ref = m[0]
#         event.gridref = new_grid_ref
#         event.save()
#         print('Updated grid ref to %s' % new_grid_ref)
#     else:
#         print('Did not match %s' % event.location)

#print_events_with_course_notes()

# Correct non-competitive results
# re_float = re.compile(r'^([0-9]{2,3}\.[0-9]{2}|100)$')
# for result in Result.objects.all():
#     if re.match(re_float, result.notes):
#         result.competitive = True
#         result.save()

# DROPBOX_URL = "https://www.dropbox.com/sh/9k1dlyc9tuuvbnm/AACuqtOceHY7e8FmEyM7Qd0Ua?dl=0"
# dropbox_files = get_docx_url_list(DROPBOX_URL)

# dir = 'C:\\Users\\Jamie\\Dropbox\\DR Run results copy\\'
# docx_files = [ f for f in listdir(dir) if isfile(join(dir,f)) ]

#populate result.position
# for event in Event.objects.all():
#     position = 1
#     for result in Result.objects.filter(event__id = event.id):
#         #result.position = position
#         #result.save()
#         print(str(position))
#         position = position + 1

# default = None
# #populate event.source field
# for event in Event.objects.all():
#     if event.source or event.results_known_to_be_missing():
#         continue
#
#     if event.date.year < 2011 or (event.date.year == 2011 and event.series.season == Series.SUMMER):
#         date_str = event.date.strftime('%d-%m-%y')
#
#         url = dropbox_files.get(date_str, default)
#         if url:
#             print(url)
#             event.source = url
#             event.save()
#
#         else:
#             print('Could not find a docx file for %s' % event)
#             print(event.notes)
#
#     else:
#         print('Need to find webpage for %s' % event)
#         search = event.series.season + "_" + str(event.date.year)
#         url = WEBPAGES[search.lower()]
#         #print(url)
#         event.source = url
#         event.save()


# Get rid of 'x Winter series - round x' from notes
# for result in Result.objects.all():
#
#     regexp = re.compile(r'\[\W[a-zA-Z]+\sWinter\s[S|s]eries\s-\sRound\s\d{1}\W\]')
#     if regexp.search(result.notes):
#         print("Found match")
#
#         test = re.sub(regexp,'', result.notes)
#         test.strip()
#         print(test)
#
#         result.notes = test
#         result.save()





# #Find events with no results and try to get the results
# dir = 'C:\\Users\\Jamie\\Dropbox\\DR Run results copy\\'
# files_to_search = [ f for f in listdir(dir) if isfile(join(dir,f)) ]
#
# all_events = Event.objects.order_by('date')
# events_to_try = []
#
# for event in all_events:
#     results = Result.objects.filter(event = event)
#     if len(results) > 0:
#         continue
#
#     if event.notes.find('Results missing') > -1 or event.notes.find('No results') > -1 or event.notes.find('Event cancelled') > -1:
#         #Don't bother searching for results if we know they don't exist
#         continue
#
#     # if event.notes.find('Run / Bike / Run') > -1:
#     #     #Ignore this event for now
#     #     continue
#
#     events_to_try.append(event)
#
#
# #for event in [events_to_try[0]]:
# for event in events_to_try:
#
#     print(str(event.date) + " - " + event.location + " - " + event.notes)
#
#     if event.date.year < 2011 or (event.date.year == 2011 and event.date.month == 1):
#         #import_docx_for_date(event, dir, files_to_search)
#         print('Need to import from docx source')
#     else:
#         print('Need to import from non-docx source')




#Update result types
# type_score = ResultDataType.objects.get(short_description = 'Score')
#
# for result in Result.objects.all():
#     if result.score:
#         result.type = type_score
#         result.save()


