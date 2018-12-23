import os

class CommonConfig:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))


class FirebaseConfig:

    DATABASE_URL = 'SECRET'
    SDK_PATH = CommonConfig.PROJECT_ROOT + "/config/course-watch-utility-adminsdk.json"


class NotificationConfig:
    API_KEY = 'SECRET'
    SENDER_ADDRESS = 'course.watch.noreply@gmail.com'
