class CourseNotFoundException(Exception):
    """
    Wrapper Exception
    """

    def __init__(self, message):
        super(CourseNotFoundException, self).__init__(message)