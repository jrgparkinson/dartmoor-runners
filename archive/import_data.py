from lxml import etree
import re
import urllib.request
import zipfile
from bs4 import BeautifulSoup
from .models import Course, Result, Runner, Event, ResultDataType


__author__ = 'Jamie'

class docx_result_file:
    def __init__(self, filename):
        self.filename = filename
        self.get_xmltree()

    def get_xmltree(self):
        #Unzip the file
        with open(self.filename, 'rb') as f:
            zip = zipfile.ZipFile(f)
            xml_content = zip.read('word/document.xml')

        #Parse as XML
        self.xmltree = etree.fromstring(xml_content)

    def get_plain_text(self):
        return etree.tostring(self.xmltree, pretty_print=True)

    @staticmethod
    def check_element_is(element, type_char):
        word_schema = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        return element.tag == '{%s}%s' % (word_schema,type_char)


    def load_table(self):
        tree = self.xmltree

        #Find the table
        for node in tree.iter(tag=etree.Element):
            if docx_result_file.check_element_is(node, 'tbl'):
                table = node
                break

        rows = []

        for el in table.iter(tag=etree.Element):
            if self.check_element_is(el, 'tr'):
                row = el

                cols = []

                for ele in row.iter(tag=etree.Element):
                    if self.check_element_is(ele, 'tc'):
                        col = ele

                        for elem in col.iter(tag=etree.Element):
                            if self.check_element_is(elem, 'p'):
                                cell = elem

                                cell_contents = ""

                                for eleme in cell.iter(tag=etree.Element):
                                    if self.check_element_is(eleme, 't'):
                                        cell_contents = cell_contents + eleme.text

                                break

                        cols.append(cell_contents)

                rows.append(cols)

        self.table = rows


def import_table(rows, event = None, first_result_row = 5):
    #Import a table in the format of a list of lists
    try:
        print(rows)
    except UnicodeEncodeError:
        print("Couldn't print rows due to unicode encode error")
        
    #Merge together empty cells
    for i in range(len(rows)):
        row = rows[i]
        if len(row) == 4 and (row[1] == '' and row[2] == '' and row[3] == ''):
            rows[i] = [row[0]]

        elif len(row) == 3 and (row[1] == '' and row[2] == ''):
            rows[i] = [row[0]]

        # elif len(row) == 2 and row[1] == '':
        #     rows[i] = [row[0]]



    if not event:
        event = Event.get_from_date_row(rows[0][0])
        if not event:
            return False

    print("Reading results for event %s" % event)

    score_row = ['', 'points', 'penalties', 'total', 'position']
    score_row_2 = ['', 'points', 'penalty', 'score', 'position']
    score_row_3 = ['', 'score', 'penalty', 'final score', 'points', 'position']
    score_row_4 = ['', 'score', 'penalty', 'final score', 'position']
    if score_row in rows \
            or score_row_2 in rows \
                    or score_row_3 in rows \
            or score_row_4 in rows:
        score_event = True
        score_column = 3
    elif ['Results','Points','',''] in rows\
            or ['','Points',''] in rows\
            or ['','score','points'] in rows:
        score_event = True
        score_column = 1
    else:
        score_event = False
        score_column = -1

    #Hard code score event
    # score_event = True
    # score_column = 1

    print("Score event? %s" % score_event)

    #Set some defaults
    course = None
    time = None
    score = None

    position = 1

    for row in rows[first_result_row:]:
        try:
            print("Reading row %s" % row)

        except UnicodeEncodeError:
            print("Skipping row to UnicodeEncodeError")
            continue

        # Skip blank rows
        if len(row) == 0:
            print("Blank - skipping")
            continue

        #Skip series title rows
        if row[0].find('Series - Round') > -1 or row[0].find('Round ') > -1\
                or row[0] == "Results" or row[0] == "":
            print("Title - skipping")
            continue

        # Find course titles
        if len(row) == 1:
            #Just check it's not the last row
            if row == rows[-1]:
                if event.notes == "":
                    print('Setting event notes equal to row')
                    event.notes = row[0]
                    event.save()
                elif event.notes.find(row[0]) == -1:
                    print('Adding row to notes')
                    event.notes = event.notes + ", " + row[0]
                    event.save()
                else:
                    print('Row already in notes')

            else:
                course = Course.objects.get_or_create(name = row[0].strip(), event = event)[0]
                print("Course - skipping")

            continue

        name = row[0]
        print("Name: %s" % name)

        #When there's a score:
        if score_event:
            notes = row[-1]
            [row[score_column], notes] = Result.extract_notes(row[score_column], notes)
            score = Result.parse_score(row[score_column])

            # if row[3]:
            #     [row[3], notes] = Result.extract_notes(row[3], notes)
            #     if row[3]:
            #         score = int(row[3])
            #     else:
            #         score = None


            competitive = True
            time = None
            type = ResultDataType.objects.get(short_description = 'Score')

        else:
            #When there's a time
            notes = row[-1]

            if notes:
                competitive = False
            else:
                competitive = True



            [row[1], notes] = Result.extract_notes(row[1], notes)
            time = Result.parse_time(row[1])
            score = None
            type = ResultDataType.objects.get(short_description = 'Time')

            if not time:
                return False


        #Find/create the runner - note that a name field may contain multiple runners if they ran together
        # [firstname, surname] = Runner.parse_name(name)
        # runner = Runner.objects.get_or_create(firstname = firstname, surname = surname)[0]
        runners = Runner.parse_name_field(name)

        if not runners:
            print("Couldn't parse name: %s" % name)
            return False


        #Update or create the result
        for runner in runners:
            result = Result.objects.update_or_create(event = event, runner = runner, order = 1, score = score, time = time, notes = notes, competitive = competitive, type = type, course = course, position = position)
            print("Inserted result")
        position = position + 1

    #Successful if we've inserted something
    if position > 1:
        return True
    else:
        return False

def get_docx_url_list(dropbox_url):
    urls = {}
    regexp = re.compile(r'https:\/\/www\.dropbox\.com\/sh\/[a-z0-9]+\/[^\/]+\/\d{3}%20(\d{2}-\d{2}-\d{2})(%20w\d)?\.docx\?dl=0')


    #Load the url
    page = urllib.request.urlopen(dropbox_url)
    contents = page.read()
    contents = contents.decode("utf-8")
    soup = BeautifulSoup(contents, 'html.parser')
    for a in soup.findAll('a', href=True):
        href = a['href']
        m = re.match(regexp, href)
        if m:
            #print(m.group(1) + " - " + href)
            #print(m)
            urls[m.group(1)] = href

    return urls

def get_docx_file_for_date(event, files_to_search):
    #Try and find a results file for this date
    date_search = event.date.strftime('%d-%m-%y')

    result_file = None
    for file in files_to_search:
        if file.find(date_search) > -1 and file.find('old') == -1:
            result_file = file

    return result_file

def parse_docx_file(result_file, dir, event=None):

    #For hardcoding the results file
    #result_file = "071 xx-04-02.docx"

    if not result_file:
        return False

    print('Found result file: %s' % result_file)

    #Try and import results
    file_location = dir + result_file
    print(file_location)
    resultFile = docx_result_file(file_location)
    resultFile.load_table()

    #Determine where the results start
    table_list = resultFile.table

    if table_list[3][0].find("Round ") == -1:
        first_result_row = 3
    else:
        first_result_row = 4


    return (table_list, first_result_row)

def parse_webpage_for_event(url, event):
    #Load the url
    page = urllib.request.urlopen(url)
    contents = page.read()
    contents = contents.decode("utf-8")
    soup = BeautifulSoup(contents, 'html.parser')

    # Find the required table
    tables = soup.find_all('table')
    for table in tables:
         # Parse table into a list of lists
        table_list = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            table_list.append(cols)

        date_cell = table_list[0][0]

        e  = Event.get_from_date_row(date_cell)
        if event == e:
            return (table_list, 3)

    return None


def import_web_page(url, table_number):

    #Load the url
    page = urllib.request.urlopen(url)
    contents = page.read()
    contents = contents.decode("utf-8")
    soup = BeautifulSoup(contents, 'html.parser')

    # Find the required table
    tables = soup.find_all('table')
    table = tables[table_number]

    # Parse table into a list of lists
    table_list = []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        table_list.append(cols)

    #print(table_list)

    #Deal with the table in a standard way
    import_table(table_list)

def parse_google_sheet(url, event):

    # Load the URL
    page = urllib.request.urlopen(url)
    contents = page.read()
    contents = contents.decode("utf-8")
    soup = BeautifulSoup(contents, 'html.parser')

    # Find out what sort of format this is
    #Find the year
    heading = soup.find('title')
    year = int(re.sub('[^0-9.]','', heading.string))

    #Is it summer or winter?
    if heading.string.find('Summer') > -1:
        summer = True
    else:
        summer = False

    print("Summer Series? %s" % summer)

    #Check what format the spreadsheet is in
    if year > 2014 or (year == 2014 and not summer):
        new_format = True
    else:
        new_format = False

    print("New Format? %s" % new_format)

    #The first table contains all the results
    table = soup.find('table',  attrs={'class':'waffle'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    # Find the column which contains the event we're interested in
    if new_format:
        date_row_index = 2
    else:
        date_row_index = 1

    cols = rows[date_row_index].find_all('td')
    start = -1
    for i in range(0, len(cols)):
        col = cols[i]
        if col.text and col.text.find('Date') == -1:
            cell_event = Event.get_from_date_row(col.text)
            if cell_event == event:
                # This is the event we're interested in, so note down the column

                #different formats
                if new_format:
                    start = i-1
                else:
                    start = i

    if start == -1:
        print('Could not find the required event in the google sheet')
        return False

    # Now we have the index of the event we want, let's compile the data into our standard format
    # We want to take the start column and up to three to it's right, as long as they're not completely empty,
    # and put this into our own table
    table_list = []
    for row in rows:

        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        row = cols[start:start+4]

        # Skip some rows
        if len(row) == 1 and row[0] == '':
            continue
        if len(row) == 2 and row[0] == '' and row[1] == '':
            continue

        table_list.append(row)

    # Remove empty columns
    for column in [3,2,1,0]:
        empty_column = True
        for row in table_list:
            if row[column]:
                empty_column = False
                break

        if empty_column:
            for row in table_list:
                del(row[column])

 
    #print(table_list)

    if new_format:
        first_results_row = 8
    else:
        first_results_row = 5

    return (table_list, first_results_row)

###############################################################################
###############################################################################

