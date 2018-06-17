
from mail_db import MailDB
import json
data = {}




# An example of passing no explicit auth
mdb = MailDB()

# An example of passing in explicit auth
with open('C:\\path\\to\\creds\\of_email.json') as f:
   data = json.load(f)


mdb = MailDB(data.get('user'),data.get("password"))

# Can insert any JSON to the mail db
insert_key ="key_four"
insert_value = {

                    "one":"two",
                    "three":"four",
                    "four": True,
                    "five": [],
                    "six":["one","two","three"],
                    "seven":7
                }

# An example of an insertion statement
print(mdb.insert(key=insert_key,value=insert_value))

# An example of a GET statement
raw_data = mdb.get(key=insert_key)
print (raw_data)

# An example of an UPDATE statement
update_value = {
    "new":"value",
    "test":123
}
print (mdb.update(key=insert_key,value=update_value))

# Requerying the database using the same key, but observe with new values
raw_data = mdb.get(key=insert_key)
print (raw_data)


# An example of an UPDATE statement on a key that does not exist
new_insertkey = "key_five"
update_value = {
    "new":"newer_value",
    "test":1234
}
print (mdb.update(key=new_insertkey,value=update_value))

# Requerying the database using the same key, but observe with new values
raw_data = mdb.get(key=insert_key)
print (raw_data)


# An example of an UPDATE statement on a key that does not exist, but force the insertion anyway
new_insertkey = "key_five"
update_value = {
    "new":"even_newer_value",
    "test":12345
}
print (mdb.update(key=new_insertkey,value=update_value,forced_insert=True))

# Requerying the database using the same key, but observe with new values
raw_data = mdb.get(key=new_insertkey)
print (raw_data)