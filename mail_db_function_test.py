
from mail_db import MailDB
import json
data = {}
with open('/Users/andrewlien/.test/creds') as f:
    data = json.load(f)


mdb = MailDB(data.get('user'),data.get("password"))


print mdb.domain

insert_key = "key"
insert_value = "value"

print mdb.insert(key=insert_key,value=insert_value)


