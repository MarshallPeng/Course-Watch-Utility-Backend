import firebase_admin
from firebase_admin import db, credentials

from src.config.config import FirebaseConfig
from src.model.CourseRequest import CourseRequest
import json
import logging

from src.model.User import User


class FirebaseDBClient():
    """
    Client to get, add, remove, courses from firebase.
    """

    def __init__(self):
        self.SDK_PATH = FirebaseConfig.SDK_PATH

        self.cred = credentials.Certificate(self.SDK_PATH)

        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(self.cred, {
                'databaseURL': FirebaseConfig.DATABASE_URL
            })

        self.db = db.reference()

    def add_course(self, course, user):
        self.db.child('users/' + str(user) + '/requests/' + course.id).set(json.loads(course.toJSON()))

    def course_exists(self, course, user):
        return self.db.child('users/' + str(user) + '/requests/' + course.id).get() is not None

    def get_courses_for_user(self, user):
        courses_dicts = self.db.child('users/' + str(user) + '/requests/').get()
        if courses_dicts is None:
            logging.info("No course watch requests detected")
            return []
        else:
            return [CourseRequest.fromJSON(dict(courses_dicts)[key]) for key in dict(courses_dicts)]

    def delete_course(self, course, user):
        self.db.child('users/' + str(user) + '/requests/' + course.id).delete()

    def get_all_users(self):
        users_dicts = self.db.child('users/').get()
        if users_dicts is None:
            return []
        else:
            return [key for key in dict(users_dicts)]
