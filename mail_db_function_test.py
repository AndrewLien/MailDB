
from mail_db import MailDB
import json
data = {}


with open('C:\\Users\\andylien.tar.gz\\Dev\\creds\\maildb.json') as f:
    data = json.load(f)


mdb = MailDB(data.get('user'),data.get("password"))


#print (mdb.domain)

#insert_key = "second_key"

insert_key ="key_one"
insert_value = {
                    "one":"two",
                    "three":"four",
                    "four": True,
                    "five": [],
                    "six":["one","two","three"],
                    "seven":7
                }

#print (mdb.insert(key=insert_key,value=insert_value))

raw_data = mdb.get(key=insert_key)
print(raw_data)
