from src.config.config import NotificationConfig
from src.config.config import CommonConfig
import logging

import sendgrid
from sendgrid.helpers.mail import *


class NotificationService:
    """
    Service to handle the sending of emails via Sendgrid
    """

    def create_email_body(self, request, enrl, lim, crn):
        """
        Creates Email body, returns as string.
        :param request:
        :param enrl:
        :param lim:
        :param crn:
        :return:
        """
        with open(CommonConfig.PROJECT_ROOT + '/../resources/email_template.txt') as fp:
            message = fp.read() \
                .replace('[subj]', request.subj) \
                .replace('[number]', request.number) \
                .replace('[prof]', request.prof) \
                .replace('[period]', request.period) \
                .replace('[enrl]', enrl) \
                .replace('[lim]', lim) \
                .replace('[crn]', crn)

        return message

    def send_mail(self, course, enrl, lim, crn):
        """
        Send email via SendGrid API
        :param course:
        :param enrl:
        :param lim:
        :return:
        """
        try:
            sg = sendgrid.SendGridAPIClient(apikey=NotificationConfig.API_KEY)

            from_email = Email(NotificationConfig.SENDER_ADDRESS)
            to_email = Email(course.email)
            subject = "There is an opening in " + str(course.subj) + str(course.number)
            content = Content("text/plain", self.create_email_body(course, enrl, lim, crn))

            mail = Mail(from_email, subject, to_email, content)

            response = sg.client.mail.send.post(request_body=mail.get())

            logging.info("Email sent")
            logging.info(response.status_code)
            logging.info(response.body)
            logging.info(response.headers)
        except Exception as e:
            logging.info(e.args)
