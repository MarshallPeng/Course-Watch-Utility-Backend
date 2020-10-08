from src.client.FirebaseDBClient import FirebaseDBClient
from src.client.FirebaseAuthClient import FirebaseAuthClient
from src.config.config import CommonConfig
from src.service.TimetableService import TimetableService
from src.exception.InvalidRequestException import InvalidRequestException
import json


class RequestStorageService:
    """
    Service to handle retrival and storage of course watch requests
    """

    def __init__(self):
        self.dbclient = FirebaseDBClient()
        self.authclient = FirebaseAuthClient()
        self.timetable_service = TimetableService()

    def add_course_request(self, course, user):
        if not self.dbclient.course_exists(course, user):
            self.dbclient.add_course(course, user)

    def get_requests_for_user(self, user):
        return self.dbclient.get_courses_for_user(user)

    def get_users(self):
        return self.dbclient.get_all_users()

    def delete_request(self, course, user):
        self.dbclient.delete_course(course, user)

    def clear_requests(self):
        self.dbclient.clear_requests()

    def is_valid_request(self, course):
        """
        Handles some basic input validation.
        Course numbers and professor names change too often to cache in json file.
        These will be handled during the actual query.
        :param text: The text message request
        :return: True if valid. False if not
        """

        with open(CommonConfig.PROJECT_ROOT + '/../resources/valid_inputs.json') as proper_inputs_file:
            proper_subjects = json.load(proper_inputs_file)

        if course.subj not in proper_subjects["Subj"]:
            raise InvalidRequestException("Subject does not exist: " + course.subj)
        if course.period not in proper_subjects["Period"]:
            raise InvalidRequestException("Period does not exist: " + course.period)

        # if not self.authclient.is_valid_user(course.email):
        #     raise InvalidRequestException(
        #         "User {0} is not Authorized. Just PM me and I'll add you".format(course.email))

        # Check if the course exists. Do the other stuff before because don't want to connect to timetable too much
        if self.timetable_service.get_course_data(course_request=course) is None:
            raise InvalidRequestException("Course does not exist in timetable")

        return True
