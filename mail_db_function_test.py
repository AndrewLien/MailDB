
from mail_db import MailDB
import json
data = {}


with open('C:\\Users\\andylien.tar.gz\\Dev\\creds\\maildb.json') as f:
    data = json.load(f)


mdb = MailDB(data.get('user'),data.get("password"))


print (mdb.domain)

insert_key = "key"
insert_value = "value"

#print (mdb.insert(key=insert_key,value=insert_value))
mdb.get(key=insert_key)

