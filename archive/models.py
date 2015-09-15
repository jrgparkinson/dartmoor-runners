from datetime import datetime
import re

from django.db import models
import inflect


# Create your models here.
#from .map_tools2 import grid_to_lat_lon
from .map_tools import os_grid_ref_to_lat_lon


class Runner(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'
    GENDERS = (
        (UNKNOWN, 'Unknown'),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    firstname = models.CharField(max_length= 255)
    surname = models.CharField(max_length= 255)
    sex = models.CharField(max_length = 1, choices = GENDERS, default = UNKNOWN)
    dob = models.DateField(blank = True, null = True)

    def __str__(self):
        return str(self.firstname) + " " + str(self.surname)

    class Meta:
        ordering = ['surname']

    def format_name(self):
        return '<a href="/archive/runner/%s">%s %s</a>' % (self.id, self.firstname, self.surname)

    @staticmethod
    def parse_name(name):
        # Remove all non alphabet characters
        regex = re.compile('[^a-zA-Z\-\s]')
        name = regex.sub('', name)
        name = name.strip() #remove white spaces
        #print(name)

        if name.find(" ") > -1:
            parts = name.split(" ")
            firstname = parts[0]
            surname = parts[1]

        else:
            firstname = name
            surname = ""

        return [firstname, surname]


    @staticmethod
    def parse_name_field(string):
        string = string.strip()

        #Special cases
        string = re.sub("(?i)De Vries", "De-Vries", string)
        string = re.sub("(?i)Du Bois", "Du-Bois", string)

        UNKNOWN_NAME = '?'

        # Remove nicknames e.g. Stewart "Rambo" Bondi
        regex_nickname = re.compile(r'"[a-zA-Z\s]+"\s')
        string = re.sub(regex_nickname, '', string)

        runners = []

        #First split the name field into the different names, if appropriate
        # regex_single_name = re.compile(r'^([a-zA-Z\-]+)\s([a-zA-Z\-\?]+)$')
        # regex_two_names = re.compile(r'^([a-zA-Z\-]+)\s([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s([a-zA-Z\-\?]+)$')
        # regex_three_names = re.compile(r'^([a-zA-Z\-]+)\s([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s([a-zA-Z\-]+)$')
        #
        # regex_two_names_same_surname = re.compile(r'^([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s([a-zA-Z\-\?]+)$')
        # regex_three_names_same_surname = re.compile(r'^([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s([a-zA-Z\-\?]+)$')
        #
        # regex_two_names_same_surname_third_name = re.compile(r'^([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s([a-zA-Z\-\?]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s([a-zA-Z\-\?]+)$')
        #
        # regex_single_no_surname =  re.compile(r'^([a-zA-Z\-]+)$')
        # regex_two_no_surname = re.compile(r'^([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)$')
        # regex_three_no_surname = re.compile(r'^([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)$')
        # regex_four_no_surname = re.compile(r'^([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)$')
        #
        # regex_two_names_first_surname = re.compile(r'^([a-zA-Z\-]+)\s([a-zA-Z\-]+)\s*(,|\sand\s|&|\/)\s*([a-zA-Z\-]+)$')

        firstname = r'([a-zA-Z\-\?]+)'
        surname = r'([a-zA-Z\-\?]+)'
        fullname = firstname + r'\s' + surname
        joiner = r'\s*(,|\sand\s|&|\/)\s*'

        regex_single_name = re.compile(r'^' + fullname + r'$')
        regex_two_names = re.compile(r'^' + fullname + joiner + fullname + r'$')
        regex_three_names = re.compile(r'^' + fullname + joiner + fullname + joiner + fullname + r'$')

        regex_two_names_same_surname = re.compile(r'^' + firstname + joiner + fullname + r'$')
        regex_three_names_same_surname = re.compile(r'^' + firstname + joiner + firstname + joiner + fullname + r'$')
        regex_five_names_same_surname = re.compile(r'^' + firstname + joiner + firstname + joiner + firstname + joiner + firstname + joiner + fullname + r'$')

        regex_two_names_same_surname_third_name = re.compile(r'^' + firstname + joiner + fullname + joiner + fullname + r'$')

        regex_single_no_surname =  re.compile(r'^' + firstname + r'$')
        regex_two_no_surname = re.compile(r'^' + firstname + joiner + firstname + r'$')
        regex_three_no_surname = re.compile(r'^' + firstname + joiner + firstname + joiner + firstname + r'$')
        regex_four_no_surname = re.compile(r'^' + firstname + joiner + firstname + joiner + firstname + joiner + firstname + r'$')

        regex_two_names_first_surname = re.compile(r'^' + fullname + joiner + firstname + r'$')
        regex_three_names_first_surname = re.compile(r'^' + fullname + joiner + firstname + joiner + firstname + r'$')

        regex_two_names_two_names_same_surname = re.compile(r'^' +  fullname + joiner + fullname + joiner + firstname + joiner + fullname + r'$')

        one_name = re.match(regex_single_name, string)
        two_names = re.match(regex_two_names, string)
        three_names = re.match(regex_three_names, string)

        two_names_same_surname = re.match(regex_two_names_same_surname, string)
        three_names_same_surname = re.match(regex_three_names_same_surname, string)
        five_names_same_surname = re.match(regex_five_names_same_surname, string)

        two_names_same_surname_third_name = re.match(regex_two_names_same_surname_third_name, string)

        two_names_first_surname = re.match(regex_two_names_first_surname, string)
        three_names_first_surname = re.match(regex_three_names_first_surname, string)

        one_no_surname = re.match(regex_single_no_surname, string)
        two_no_surname = re.match(regex_two_no_surname, string)
        three_no_surname = re.match(regex_three_no_surname, string)
        four_no_surname = re.match(regex_four_no_surname, string)

        two_then_two_same_surname = re.match(regex_two_names_two_names_same_surname, string)

        if one_name:
            firstname = one_name.group(1)
            surname = one_name.group(2)
            runner = Runner.get_for_names(firstname, surname)
            runners.append(runner)

        elif two_names:
            for i in [1,4]:
                firstname = two_names.group(i)
                surname = two_names.group(i+1)
                runner = Runner.get_for_names(firstname, surname)
                runners.append(runner)

        elif three_names:
            for i in [1,4,7]:
                firstname = three_names.group(i)
                surname = three_names.group(i+1)
                runner = Runner.get_for_names(firstname, surname)
                runners.append(runner)

        elif two_then_two_same_surname:
            for i in [1,4]:
                firstname = two_then_two_same_surname.group(i)
                surname = two_then_two_same_surname.group(i+1)
                runner = Runner.get_for_names(firstname, surname)
                runners.append(runner)

            for i in [7, 9]:
                firstname = two_then_two_same_surname.group(i)
                surname = two_then_two_same_surname.group(10)
                runner = Runner.get_for_names(firstname, surname)
                runners.append(runner)

        elif two_names_first_surname:
            firstname = two_names_first_surname.group(1)
            surname = two_names_first_surname.group(2)
            runner = Runner.get_for_names(firstname, surname)
            runners.append(runner)

            firstname = two_names_first_surname.group(4)
            runner = Runner.get_for_names(firstname, UNKNOWN_NAME)
            runners.append(runner)

        elif three_names_first_surname:
            firstname = three_names_first_surname.group(1)
            surname = three_names_first_surname.group(2)
            runner = Runner.get_for_names(firstname, surname)
            runners.append(runner)

            for i in [4, 6]:
                firstname = three_names_first_surname.group(i)
                runner = Runner.get_for_names(firstname, UNKNOWN_NAME)
                runners.append(runner)

        elif two_names_same_surname:
            for i in [1,3]:
                firstname = two_names_same_surname.group(i)
                surname = two_names_same_surname.group(4)
                runner = Runner.get_for_names(firstname, surname)
                runners.append(runner)

        elif two_names_same_surname_third_name:
            for i in [1,3]:
                firstname = two_names_same_surname_third_name.group(i)
                surname = two_names_same_surname_third_name.group(4)
                runner = Runner.get_for_names(firstname, surname)
                runners.append(runner)

            #Third name
            firstname = two_names_same_surname_third_name.group(6)
            surname = two_names_same_surname_third_name.group(7)
            runner = Runner.get_for_names(firstname, surname)
            runners.append(runner)

        elif three_names_same_surname:
            for i in [1,3,5]:
                firstname = three_names_same_surname.group(i)
                surname = three_names_same_surname.group(6)
                runner = Runner.get_for_names(firstname, surname)
                runners.append(runner)

        elif five_names_same_surname:
            for i in [1,3,5,7,9]:
                firstname = five_names_same_surname.group(i)
                surname = five_names_same_surname.group(10)
                runner = Runner.get_for_names(firstname, surname)
                runners.append(runner)


        elif one_no_surname:
            firstname = one_no_surname.group(1)
            runner = Runner.get_for_names(firstname, UNKNOWN_NAME)
            runners.append(runner)

        elif two_no_surname:
            for i in [1,3]:
                firstname = two_no_surname.group(i)
                runner = Runner.get_for_names(firstname, UNKNOWN_NAME)
                runners.append(runner)

        elif three_no_surname:
            for i in [1,3,5]:
                firstname = three_no_surname.group(i)
                runner = Runner.get_for_names(firstname, UNKNOWN_NAME)
                runners.append(runner)

        elif four_no_surname:
            for i in [1,3,5,7]:
                firstname = four_no_surname.group(i)
                runner = Runner.get_for_names(firstname, UNKNOWN_NAME)
                runners.append(runner)

        else:
            runners = None
            print('No regex match for "%s"' % string)

        return runners

    @staticmethod
    def get_for_names(firstname, surname):
        print('Get runner for firstname: %s, surname: %s' % (firstname, surname))
        #First try and get runner from the runner table
        runner = Runner.objects.filter(firstname = firstname, surname = surname)
        if runner:
            return runner[0]

        #Now see if we can find an alias
        alias = Alias.objects.filter(firstname = firstname, surname = surname)
        if alias:
            return alias[0].runner

        #If we still don't have a runner, create one and save it to the DB
        runner = Runner(firstname = firstname, surname = surname)
        runner.save()
        return runner

class Alias(models.Model):
    firstname = models.CharField(max_length= 255)
    surname = models.CharField(max_length= 255)
    runner = models.ForeignKey(Runner)

    def __str__(self):
        return self.firstname + " " + self.surname

class Series(models.Model):
    #Hard code seasons
    WINTER = 'Winter'
    SUMMER = 'Summer'
    SEASONS = (
        (WINTER, 'Winter'),
        (SUMMER, 'Summer')
    )

    number = models.IntegerField(default = -1)
    season = models.CharField(max_length = 20, choices = SEASONS, default = WINTER)
    year = models.IntegerField(default = 1900)

    def __str__(self):
        if self.number == -1:
            return "Unknown series"
        else:
            return self.number_desc() + " " + self.season + " series " + "(" + str(self.year)    + ")"

    def number_desc(self):
        p = inflect.engine()
        return p.ordinal(self.number)

    def num_events(self):
        events = Event.objects.filter(series = self)
        num_events = len(events)
        return num_events

    def is_winter(self):
        return self.season == self.WINTER

    def hyperlink_name(self):
        return "<a href='/archive/series/"+ str(self.id) +"/'>" + self.__str__()  + "</a>"


class Course(models.Model):
    event = models.ForeignKey('Event')
    name = models.CharField(max_length = 500)

    def __str__(self):
        string = self.name + " (" + str(self.event) + ")"
        return string

    def get_results(self):
        results = Result.objects.filter(course__id = self.id)
        results_list = Result.collate_result_set(results)
        return results_list


class Event(models.Model):
    location = models.CharField(max_length = 255)
    lat = models.FloatField(default = None, null = True, blank=True)
    lon = models.FloatField(default = None, null = True, blank=True)
    date = models.DateField(default = '1900-01-01')
    series_number = models.IntegerField(default = -1)
    series = models.ForeignKey(Series, default=-1)
    organisers = models.ManyToManyField(Runner)
    old_number = models.IntegerField(default = -1)
    number = models.IntegerField(default = -1)
    number_increment = models.IntegerField(default = 1) # Some events shouldn't have a run number
    gridref = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null = True, blank = True)
    source = models.TextField(null = True, blank=True, default=None)


    def __str__(self):
        return str(self.date) + " - " + str(self.location)

    class Meta:
        ordering = ['date']

    def link(self):
        return "/archive/event/" + str(self.id)

    def gridref_hyperlink(self):
        string = "<a href='http://gridreferencefinder.com/osfs/?gr="+ str(self.gridref) +"|"+ str(self.gridref) +"|1&v=h'>" + str(self.gridref) + "</a>"
        return string

    def results_known_to_be_missing(self):
        search_strings =['Results missing', 'No results', 'Event cancelled']

        if any(x in self.notes for x in search_strings):
            return True
        else:
            return False

    def make_lat_lon(self):
        re_gridref = re.compile(r'^SX([0-9]{3})([0-9]{3})$')
        east_north = re.match(re_gridref, str(self.gridref))
        if not east_north:
            return

        #We have a valid gridref, continue
        lat, lon = os_grid_ref_to_lat_lon(self.gridref)
        #lat, lon = grid_to_lat_lon(self.gridref)
        self.lat = lat
        self.lon = lon
        self.save()


    # Delete all results and courses for this event
    def delete_past_results(self):
        past_results = Result.objects.filter(event_id = self.id)
        for res in past_results:
            res.delete()

        courses = Course.objects.filter(event_id = self.id)
        for course in courses:
            course.delete()

    def calculate_points(self):
        print("Calculating points for event %s" % self)
        # There may be different sets of results, need to compare within a set of results
        for order in [1,2,3,4,5]:

            results = Result.objects.filter(event_id = self.id, order = order).order_by('time')
            print("Got %d results for order %d" % (len(results), order))

            #Find the quickest competitive result
            leading_result = None
            for res in results:
                if res.competitive:
                    leading_result = res
                    print('Found leading result %s' % res)
                    break


            if leading_result == None\
                or (leading_result.type.type == ResultDataType.TIME and not leading_result.time)\
                    or (leading_result.type.type == ResultDataType.TIME and leading_result.time.seconds == 0)\
                    or (leading_result.type.type == ResultDataType.SCORE and (leading_result.score == 0 or leading_result.score == None)):

                continue

            # Now calculate the points - percentage of leading time/score
            for res in results:
                if res.type != leading_result.type:
                    print('Warning - found a result of different type to the leading result')
                    continue

                if res.competitive:
                    if res.type.type == ResultDataType.TIME and res.time.seconds != 0:
                        points = 100 * leading_result.time/res.time

                    elif res.type.type == ResultDataType.SCORE and res.score:
                        points = 100 * res.score/leading_result.score

                    else:
                        print("Warning - unexpected result type %s" % res.type)
                        points = 0

                else:
                    points = 0


                points = round(points, 2)
                res.points = points
                res.save()
                #print(points)

    def remove_points_from_notes(self):
        results = Result.objects.filter(event_id = self.id)

        for res in results:
            if not res.points:
                continue

            points = "%.2f" % float(res.points)
            res.notes = res.notes.replace(points, '')
            res.save()

    @staticmethod
    def get_from_date_row(string):
        string = string.strip()
        m = re.match(r'(\d+\s+[a-zA-z]+\s+\d{4})',  string)
        if m:
            raw_date = m.group(0)
            date = datetime.strptime(raw_date, "%d %B %Y")
            event = Event.objects.get(date = date)
            return event
        else:
            print("Couldn't parse %s" % string)
            return

    class Admin:
        list_display = ('date', 'location', 'gridref', 'series','number', 'notes')
        list_filter = ('date', 'location', 'series','number',)
        ordering = ('date')
        search_fields = ('location')

class ResultDataType(models.Model):
    #Hard code result types
    SCORE = 'score'
    TIME = 'time'
    DATA_TYPES = (
        (TIME, 'Time'),
        (SCORE, 'Score')
    )

    type = models.CharField(max_length=20, choices = DATA_TYPES, default = TIME)
    short_description = models.CharField(max_length=50)
    long_description = models.TextField(blank = True, null = True)

    def __str__(self):
        return self.short_description

class Result(models.Model):
    event = models.ForeignKey(Event)
    runner = models.ForeignKey(Runner)
    time = models.DurationField(blank = True, null = True)
    score = models.IntegerField(blank = True, null = True)
    competitive = models.BooleanField(default=True)
    type = models.ForeignKey(ResultDataType, default=1)
    course = models.ForeignKey(Course, blank = True, null = True, default = None) #Some events have multiple courses
    order = models.IntegerField(default = 1)
    notes = models.TextField(default="", blank = True, null = True)
    position = models.FloatField(default = 999) #Determine order of results per event
    points = models.FloatField(default = None, blank=True, null=True)

    def __str__(self):
        return self.get_formatted_time()

    def get_formatted_time(self):
        return str(self.time)

    def formatted_time_score(self):
        if self.time:
            return self.get_formatted_time()
        elif self.score:
            return str(self.score)
        else:
            return "--"

    @staticmethod
    def parse_score(string):
        if not string:
            return None
        else:
            return int(string)

    @staticmethod
    def collate_result_set(results):
        results_list = []
        for result in results:

            found_runner = False
            for row in results_list:
                if row[0].runner == result.runner:
                    found_runner = True
                    row.append(result)

            if not found_runner:
                results_list.append([result])

        #Within the results for one runner, ensure they are order
        for result_row in results_list:
            result_row.sort(key = lambda x: x.order)

        return results_list


    @staticmethod
    def parse_time(string):
        string = string.strip()
        string = re.sub(r'=','',string)
        string = re.sub(r';',':',string)

        if re.search('\d?\d:\d\d:\d\d$', string):
            #It's a time
            time = datetime.strptime(string, '%H:%M:%S')

        elif re.search('\d?\d\.\d\d\.\d\d$', string):
            time = datetime.strptime(string, '%H.%M.%S')

        elif re.search('\d?\d\.\d\d\:\d\d$', string):
            time = datetime.strptime(string, '%H.%M:%S')

        elif re.search('\d?\d\:\d\d\.\d\d$', string):
            time = datetime.strptime(string, '%H:%M.%S')
            score = "Null"
        elif re.search('\d?\d:\d\d$', string):
            time = datetime.strptime(string, '%H:%M')

        elif re.search('\d?\d\.\d\d$', string):
            if float(string) < 10:
                #Assume we have hours.minutes (i.e. that no-one takes over 10 hours)
                time = datetime.strptime(string, '%H.%M')
            else:
                #Assume we have minutes.seconds
                time = datetime.strptime(string, '%M.%S')

        elif re.search('\dhrs?\s\d+', string):
            #2hrs 14, for example
            m = re.match('(\d)hrs?\s(\d+)', string)
            if m:
                hours = m.group(1)
                min = m.group(2)
                time = datetime.strptime(hours + ":" + min, "%H:%M")
            else:
                print("Couldn't parse time %s" % string)
                return None
        elif not string:
            time = datetime.strptime('00:00:00', '%H:%M:%S')
        else:
            print("Couldn't parse time %s" % string)
            return None

        zero_time = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        delta_time = time - zero_time

        return delta_time

    @staticmethod
    def extract_notes(string, notes):
        #move any text to the notes column
        m = re.match('([a-zA-Z\s\?]+)', string)
        if m:
            text = m.group(0)
            notes = notes + "(" + text + ")"
            string = string.replace(text, '')

        return[string, notes]

    @staticmethod
    def time_to_seconds(time):
        zero_time = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        delta_time = time - zero_time

        seconds = delta_time.total_seconds()

        return seconds

    def hyperlink_name(self):
        return self.runner.format_name()


