import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

from firebase_admin import auth, credentials
import firebase_admin
from src.config.config import FirebaseConfig
import logging


class FirebaseAuthClient:
    """
    Basic client to validate users via firebase auth.
    """

    def __init__(self):
        self.SDK_PATH = FirebaseConfig.SDK_PATH
        self.cred = credentials.Certificate(self.SDK_PATH)

        try:
            firebase_admin.get_app()
        except ValueError:
            firebase_admin.initialize_app(self.cred)

        self.auth = auth

    def is_valid_user(self, email):
        """
        Check to see that user is a person that I've registered, not some rando.
        If firebase can't find, then will throw exception and return false.
        :param email:
        :return:
        """
        try :
            self.auth.get_user_by_email(email)
        except auth.AuthError as e:
            logging.info(e.message)
            return False

        return True
