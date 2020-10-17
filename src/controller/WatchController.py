from src.model.User import User
from src.service.RequestStorageService import RequestStorageService
from src.service.TimetableService import TimetableService
from src.service.NotificationService import NotificationService
from src.model.CourseRequest import CourseRequest
from src.util.ResponseUtil import ResponseUtil
from src.exception.InvalidRequestException import InvalidRequestException
import logging
import datetime


class WatchController:

    def __init__(self):
        self.request_service = RequestStorageService()
        self.timetable_service = TimetableService()
        self.notification_service = NotificationService()
        self.response_util = ResponseUtil()

    def new_request(self, data):
        """
        create new course watch request, after validation
        :param data:
        :return:
        """

        course = CourseRequest.fromJSON(data['course_request'])
        user = User.fromJSON(data['user'])
        order = data['order']

        try:
            self.request_service.is_valid_request(course)
            self.request_service.add_course_request(course, user)

        except InvalidRequestException as e:
            response = self.response_util.build_error_response(code=400,
                                                               message="Course request not valid: " + e.message)
            logging.warning(e.message)
            return response

        except Exception as e:
            response = self.response_util.build_error_response(code=500, message="An Error Occurred: " + e.message)
            logging.error(e.message)
            return response

        response = self.response_util.build_success_response(code=200, message="Request Added", data={})
        logging.info(response)
        return response

    def check_courses(self):
        """
        Loops through each request loaded in storage service,
        Checks for vacancies
        Notifies user if there is an opening.
        """

        try:
            openings_detected = []
            for user in self.request_service.get_users():
                for request in self.request_service.get_requests_for_user(user):

                    logging.info("Checking class: " + str(request))
                    current_course_status = self.timetable_service.get_course_data(request)
                    enrl = current_course_status["Enrl"]
                    lim = current_course_status["Lim"]
                    crn = "CRN"  # CRN is removed from timetable during the term

                    # TODO: Fix error where enrl doesn't exist / CRN doesn't exist cuz registration hasn't opened.
                    # TODO: Need to detect when course registration has opened. Possibly deny at time of request.
                    if current_course_status.has_key('CRN'):
                        crn = current_course_status['CRN']

                    logging.info(request.subj + request.number + ": Currently Enrolled: " + enrl + " Limit: " + lim)

                    if float(enrl) < float(lim):
                        logging.info("Opening detected. Sending notification")
                        self.notification_service.send_mail(request, enrl, lim, crn)
                        self.request_service.delete_request(request, user)
                        openings_detected.append(request.__dict__)
                        logging.info("Notification sent to " + request.email)

        except Exception as e:
            response = self.response_util.build_error_response(code=500, message="An Error Occurred: " + e.message)
            logging.error(e.message)
            return response

        return self.response_util.build_success_response(code=200, message="Finished Checking Courses",
                                                         data={"openings": openings_detected})

    def get_current_requests(self, data):
        """
        Simply returns a list of all the course watch requests in firebase.
        :return:
        """
        logging.info("getting current requests for {0}".format(data))
        try:
            user = User.fromJSON(data)
            current_courses = self.request_service.get_requests_for_user(user)
            data = [course.toJSON() for course in current_courses]
        except Exception as e:
            response = self.response_util.build_error_response(code=500, message="An Error Occurred: " + e.message)
            return response
        return self.response_util.build_success_response(code=200, message="Retrieved current requests", data=data)

    def reset_requests(self):
        logging.info("Resetting course requests for the term")

        if not (datetime.datetime.today().day == 15 and datetime.datetime.today().month in [2, 5, 7, 10]):
            return self.response_util.build_error_response(code=400, message="Can't reset at this time. Good try tho :P")

        try:
            self.request_service.clear_requests()
        except Exception as e:
            response = self.response_util.build_error_response(code=500, message="An Error Occurred: " + e.message)
            logging.error(e.message)
            return response
        return self.response_util.build_success_response(code=200, message="Courses Successfully Reset")