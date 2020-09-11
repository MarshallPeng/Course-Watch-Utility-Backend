class User:
    """
    Basic model for account of user who submitted course request
    """

    def __init__(self, email=None, uid=None):
        self.account_email = email
        self.uid = uid

    def __str__(self):
        return self.account_email.replace(".", "-") + "|" + self.uid

    def generate_id(self):\
        return self.account_email.replace(".", "-") + "|" + self.uid

    @staticmethod
    def fromJSON(json_map):
        user = User()
        for key, value in json_map.items():
            user.__dict__[key] = value
        return user
