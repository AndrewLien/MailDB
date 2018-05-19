import smtplib
from email.mime.text import MIMEText

class GmailHandler():
    @staticmethod
    def get_smtp_info():
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465
        return smtp_ssl_host,smtp_ssl_port



class Errors():
    @staticmethod
    def bad_email_domain(specific_message=None):
        """
        :param specific_message:
        :return error message:
        """
        return "INVALID"
    @staticmethod
    def missing_value(specific_message=None):
        return "Missing value : {}".format(specific_message)

class Helpers():
    @staticmethod
    def retrieve_domain(email_string):
        """

        :param email_string:
        :return boolean:
        """
        if not '@' in email_string:
            return Errors.bad_email_domain()

        domain = email_string.split('@')[1]
        return domain

class MailDB():
    def __init__(self,username,password):
        self.user_name = username
        self.pass_word = password
        self.domain = Helpers.retrieve_domain(self.user_name)

        if 'gmail' in self.domain:
            self.smtp_ssl_host, self.smtp_ssl_port = GmailHandler.get_smtp_info()

    def insert(self,key=None,value=None):
        if self.domain == "INVALID":
            return 'Email State: {}'.format(Errors.bad_email_domain())

        if not key:
            return Errors.missing_value(specific_message="Requires key")
        if not value:
            return Errors.missing_value(specific_message="Requires value")

        subject = key
        body = value
        sender = self.user_name
        targets = self.user_name
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['To'] = targets

        server = smtplib.SMTP_SSL(self.smtp_ssl_host,self.smtp_ssl_port)
        server.login(self.user_name,self.pass_word)
        server.sendmail(sender,targets,msg.as_string())
        server.quit()


