import smtplib
from email.mime.text import MIMEText
import logging
import sys
import time
from itertools import chain
import email
import imaplib


class GmailHandler():
    @staticmethod
    def get_smtp_info():
        smtp_ssl_host = 'smtp.gmail.com'
        smtp_ssl_port = 465
        imap_ssl_host = 'imap.gmail.com'
        imap_ssl_port = 993

        return smtp_ssl_host,smtp_ssl_port, imap_ssl_host,imap_ssl_port



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

    @staticmethod
    def search_string(uid_max,criteria):
        c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
        return '(%s)' % ' '.join(chain(*c))

    @staticmethod
    def get_first_text_block(msg):
        type = msg.get_content_maintype()

        if type == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()

        elif type == 'text':   
            return msg.get_payload()

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
        criteria = {
            'FROM': self.user_name,
            'SUBJECT':key
        }

        uid_max = 0

        server = imaplib.IMAP4_SSL(self.imap_ssl_host,self.imap_ssl_port)
        server.login(self.user_name,self.pass_word)
        server.select('INBOX')

        result, data = server.uid('search', None, Helpers.search_string(uid_max, criteria))
        msg = email.message_from_string(data[0][1])
        print (result)
        print (data)
        print (email.message_from_string(data[0][1]))
        print (Helpers.get_first_text_block(msg))
        server.logout

        
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
        try:
            server.login(self.user_name,self.pass_word)
        except smtplib.SMTPAuthenticationError as e:
            self.logger.error('Google blocks sign-in attempts from apps that do not use modern security standards. To turn on/off this safety feature, go to https://www.google.com/settings/security/lesssecureapps and select "Turn On"')
            server.quit()
            sys.exit(1)
        server.sendmail(sender,targets,msg.as_string())
        server.quit()
        return True


