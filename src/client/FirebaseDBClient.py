import firebase_admin
from firebase_admin import db, credentials

from src.config.config import FirebaseConfig
from src.model.CourseRequest import CourseRequest
import json
import logging

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

    def add_course(self, course):
        self.db.child('requests/' + course.id).set(json.loads(course.toJSON()))

    def course_exists(self,course):
        return self.db.child('requests/' + course.id).get() is not None

    def get_all_courses(self):
        courses_dicts = self.db.child('requests/').get()
        if courses_dicts is None:
            logging.info("No course watch requests detected")
            return []
        else:
            return [CourseRequest.fromJSON(dict(courses_dicts)[key]) for key in dict(courses_dicts)]


    def delete_course(self, course):
        self.db.child('requests/' + course.id).delete()