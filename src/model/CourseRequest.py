class CourseRequest:
    """
    Basic model for a course request. Basically the info from the form.
    """

    def __init__(self, subj=None, number=None, prof=None, period=None, email=None):
        self.subj = subj
        self.number = number
        self.prof = prof
        self.period = period
        self.email = email
        self.id = self.generate_id()

    def __str__(self):
        return self.subj + "|" + self.number + "|" + self.prof + "|" + self.period + "|" + self.email

    def generate_id(self):
        """
        Creates an ID to used in firebase database
        :return:
        """
        self.id = (str(self.subj) + "-" + str(self.number) + "-" + str(self.prof) + "-" + str(self.period) + "-" + str(
            self.email)).replace(".", "-")

    def toJSON(self):
        import json
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)

    @staticmethod
    def fromJSON(json_map):
        course = CourseRequest()
        for key, value in json_map.items():
            course.__dict__[key] = value
        course.generate_id()
        return course
