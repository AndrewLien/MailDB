import smtplib
from email.mime.text import MIMEText
import logging
import sys
import time
from itertools import chain
import email
import imaplib
from email.parser import HeaderParser
import json
from copy import deepcopy

class GmailHandler():
    @staticmethod
    def get_smtp_info():
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465
        imap_ssl_host = 'imap.gmail.com'
        imap_ssl_port = 993
        imap_search_key = "X-GM-RAW"

        return smtp_ssl_host,smtp_ssl_port, imap_ssl_host,imap_ssl_port

    @staticmethod
    def get_search_key():
        return "X-GM-RAW"

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

    @staticmethod
    def key_exists(specific_message=None):
        return {"msg":"Key exists in DB : {}".format(specific_message)}

    @staticmethod
    def invalid_key(specific_message=None):
        return {'valid_key': "Key not valid", 'msg': "Key does not exist in the database", "specific_message": "{} does not exist".format(specific_message)}

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

    @staticmethod
    def return_valid_emails():
        """
        :return list
        """
        valid_emails = [
            "gmail"
        ]

    @staticmethod
    def valid_key_structure():
        """
        :returns dict
        """

        return {"valid_key":"Key not valid","msg":""}
class MailDB():
    def __init__(self,username,password):
        self.user_name = username
        self.pass_word = password
        self.domain = Helpers.retrieve_domain(self.user_name)
        self.logger = logging.getLogger('MailDB')
        
        if 'gmail' in self.domain:
            self.smtp_ssl_host, self.smtp_ssl_port, self.imap_ssl_host, self.imap_ssl_port = GmailHandler.get_smtp_info()



    def get(self,key=None):
        if not key:
            return Errors.missing_value(specific_message="Requires Key")


        server = imaplib.IMAP4_SSL(self.imap_ssl_host,self.imap_ssl_port)
        server.login(self.user_name,self.pass_word)
        server.select('"[Gmail]/All Mail"')

        search_key = 'Subject'

        if 'gmail' in self.domain:
            search_key = GmailHandler.get_search_key()
        
        result, data = server.uid('search', None, r'{} "subject:\"{}\""'.format(search_key,key))
        document_results = None
        if result == 'OK':
            
            split_data = data[0].split()
            if len(split_data) == 0:
                return Errors.invalid_key(specific_message="{}".format(key))
            fetch_num = split_data[-1]
            result,data = server.uid('fetch', fetch_num, '(RFC822)')
            
            header_data = data[0][1].decode('utf-8')

            parser = HeaderParser()
            msg = parser.parsestr(header_data)
            document_results = msg.get_payload()

        server.logout

        if document_results:
            return json.loads(document_results)
        

    def validate_key(self,key=None):
        if not key:
            return Errors.missing_value(specific_message="Requires key")

        get_key = self.get(key=key)
        
        if get_key:
            if get_key.get('valid_key') == "Key not valid":
                if get_key.get('valid_key') == True:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    def insert(self,key=None,value=None):
        if self.domain == "INVALID":
            return 'Email State: {}'.format(Errors.bad_email_domain())

        if not key:
            return Errors.missing_value(specific_message="Requires key")
        if not value:
            return Errors.missing_value(specific_message="Requires value")


        try:
            body = json.dumps(value)
        except Exception as e:
            return Errors.missing_value(specific_message="Value must be in valid JSON format")

        # Before we do anything, we need to make sure the key doesn't already exist
        if self.validate_key(key=key):
            return Errors.key_exists(specific_message='{}'.format(key))


        # Declare variables to prep for email send
        subject = key
        sender = self.user_name
        targets = self.user_name
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['To'] = targets

        server = smtplib.SMTP_SSL(self.smtp_ssl_host,self.smtp_ssl_port)
        try:
            server.login(self.user_name,self.pass_word)
        except smtplib.SMTPAuthenticationError as e:
            self.logger.error('Google blocks sign-in attempts from apps that do not use modern security standards. To turn on/off this safety feature, go to https://www.google.com/settings/security/lesssecureapps and select "Turn On"')
            server.quit()
            sys.exit(1)
        server.sendmail(sender,targets,msg.as_string())
        server.quit()
        return True


