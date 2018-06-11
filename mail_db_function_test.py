
from mail_db import MailDB
import json
data = {}


with open('C:\\path\\to\\creds\\of_email.json') as f:
    data = json.load(f)


mdb = MailDB(data.get('user'),data.get("password"))


# Can insert any JSON to the mail db
insert_key ="key_one"
insert_value = {
                    "one":"two",
                    "three":"four",
                    "four": True,
                    "five": [],
                    "six":["one","two","three"],
                    "seven":7
                }

# An example of an insertion statement
mdb.insert(key=insert_key,value=insert_value)

# An example of a GET statement
raw_data = mdb.get(key=insert_key)

