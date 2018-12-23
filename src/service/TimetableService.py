from bs4 import BeautifulSoup
import requests
import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()
import logging

class TimetableService:
    """
    Service to read the timetable via post requests and beautiful soup HTML parser
    """

    def get_course_data(self, course_request):
        """
        Post request to timetable, then parse html
        :param course_request:
        :return:
        """

        # get page source and create parser
        logging.info("Making POST request for " + str(course_request))
        search_results = requests.post('http://oracle-www.dartmouth.edu/dart/groucho/timetable.course_quicksearch',
                             data={'subj': course_request.subj, 'crsenum': course_request.number, "classyear": "2008"}).text

        soup = BeautifulSoup(search_results, 'html.parser')
        row_data = soup.find("div", {"class": "data-table"}).tr
        column_names = [th.text.encode('ascii', 'ignore') for th in row_data.find_all('th')]

        # get table data (mainly column names)
        column_name_to_index = {}
        for index, name in enumerate(column_names):
                column_name_to_index[index] = name

        row_data = row_data.next_sibling.next_sibling.next_sibling.next_sibling

        # parse row data, store in dictionary
        while row_data:
            td_list = row_data.find_all('td')
            course_data = {}

            for index, data in enumerate(td_list):
                course_data[column_name_to_index[index]] = data.text.encode('ascii', 'ignore')

            if self.request_matches_course(course_data, course_request):
                return course_data

            row_data = row_data.next_sibling.next_sibling

        logging.info("Could not find course.")
        return None


    def request_matches_course(self, course_timetable, course_request):
        """
        Checks if a request matches a course
        :param course_timetable: course data from the timetable
        :param course_request: course data from request
        :return:
        """

        return course_timetable["Subj"] == course_request.subj and \
            float(course_timetable["Num"]) == float(course_request.number) and \
            course_timetable["Period"] == course_request.period and \
            course_request.prof.lower() in course_timetable["Instructor"].lower()