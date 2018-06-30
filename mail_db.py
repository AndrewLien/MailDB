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
import os
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
    def key_does_not_exists(specific_message=None):
        return {"msg":"Key does exists in DB, maybe you meant to perform an insert? : {}".format(specific_message)}

    @staticmethod
    def invalid_key(specific_message=None):
        return {'valid_key': "Key not valid", 'msg': "Key does not exist in the database", "specific_message": "{} does not exist".format(specific_message)}

    @staticmethod
    def invalid_creds(specific_message=None):
        return {
            "invalid":True,
            "msg":"Error retrieving email credentials. You have a few options to instantiate your session, ordered by precedence: \n  \
            1. You may also provide explicit credentials in the form of MailDB(username_string,password_string) \n  \
            2. You may instantiate MailDB() without any arguments if there exists a ~/.maildb/creds.json that contains the credentials of your email account. \n \
            \t2a. The credentials file should be in a keyvalue pair format such as: {'user':'yourusername','password':'yourpassword'}\n \
            3. You may also provide the following environment variables: MAILDB_ENV_USER, MAILDB_ENV_PASSWORD \n \
            Note: Please make sure you use your email user's full email address such as: maildb@gmail.com or maildb@outlook.com\n"
        }
    
    @staticmethod
    def invalid_json(specific_message=None):
        return {
            "msg":"Credentials file does not pass JSON validation. The credentials file should have the following format: {'user':'yourusername','password':'yourpassword'}"
        }
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

    @staticmethod
    def check_credential_path(credential_path=None):
        path = None
        default_credential_path = os.path.join(os.path.expanduser('~'), '.maildb','creds.json')  
        if credential_path is None:
            path = default_credential_path
        else:
            path = credential_path

        if os.path.isfile(path):
            creds_file = open(path,'r').read()
        else:
            return None

        try:
            creds_json = json.loads(creds_file)
        except:
            Errors.invalid_json()
            sys.exit()
        return creds_json
class Auth(): 
    def __init__(self):
        pass  

    def retrieve_auth(self,username=None,password=None,credential_path=None):
        # If either user or pass is not available, attempt to check using preconfigured JSON variables
        if username is None or password is None:
            path_results = Helpers.check_credential_path(credential_path)
            if path_results is None: 
                return Errors.invalid_creds()
            else:
                user_name = path_results.get('user')
                pass_word = path_results.get('password')
        else:
            user_name = username
            pass_word = password
        domain = Helpers.retrieve_domain(user_name)

        auth_obj = {
            "user_name": user_name,
            "pass_word": pass_word,
            "domain":domain
        }
        return auth_obj

class MailDB():
    def __init__(self,username=None,password=None,credential_path=None):
        self.logger = logging.getLogger('MailDB')

        auth_obj = Auth.retrieve_auth(username,password,credential_path)

        if auth_obj.get('invalid'):
            if auth_obj['invalid'] == True:
                self.logger.error(auth_obj.get('msg'))

        try:
            self.user_name = auth_obj.get('user_name')
            self.pass_word = auth_obj.get('pass_word')
            self.domain = auth_obj.get('domain')
        
            if 'gmail' in self.domain:
                self.smtp_ssl_host, self.smtp_ssl_port, self.imap_ssl_host, self.imap_ssl_port = GmailHandler.get_smtp_info()
        except Exception as e:
            self.logger.error(e)

    def delete(self,key=None):
        if not key:
            return Errors.missing_value(specific_message="Requires Key")


        server = imaplib.IMAP4_SSL(self.imap_ssl_host,self.imap_ssl_port)
      
        try:
            server.login(self.user_name,self.pass_word)
        except:
            self.logger.error("ERRORFATAL: Error logging in, perhaps credentials issue?")
            sys.exit()
        server.select('"[Gmail]/All Mail"')

        search_key = 'Subject'

        if 'gmail' in self.domain:
            search_key = GmailHandler.get_search_key()
        
        result, data = server.uid('search', None, r'{} "subject:\"{}\""'.format(search_key,key))
        document_results = None
        deletion_count = 0
        if result == 'OK':
            
            split_data = data[0].split()
            if len(split_data) == 0:
                return Errors.invalid_key(specific_message="{}".format(key))

            for emails in split_data:                
                server.uid('STORE', emails, '+X-GM-LABELS', '\\Trash')
                deletion_count +=1
            
        server.select('[Gmail]/Trash')  # select all trash
        server.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
        server.expunge()  # not need if auto-expunge enabled

        server.logout
        self.logger.info("Deleted 1 entries in the database, also removed {} historical entries.".format(deletion_count,deletion_count-1))
        return {"msg":"Deleted {} entries in the database".format(deletion_count)}
        

    def get(self,key=None):
        if not key:
            return Errors.missing_value(specific_message="Requires Key")


        server = imaplib.IMAP4_SSL(self.imap_ssl_host,self.imap_ssl_port)
      
        try:
            server.login(self.user_name,self.pass_word)
        except:
            self.logger.error("ERRORFATAL: Error logging in, perhaps credentials issue?")
            sys.exit()
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

    def update(self,key=None,value=None,forced_insert=False):
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
        if not self.validate_key(key=key) and forced_insert==False:
            return Errors.key_does_not_exists(specific_message='{}'.format(key))


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


