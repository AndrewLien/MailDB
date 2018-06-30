# Mail DB

A hacky library that leverages your existing email address as the backend for storing and retrieving JSON structures. 

## Getting Started

Clone the repository and start using mail_db! I aim to encapsulate this project in one file, and using the python standard libraries. This project does not store your credentials in any way 

### Prerequisites

Python 3.6+

### Installing

You need to instantiate the code by creating an object with your email address' username and password. In this example, I stored the user and pass in a JSON file and retrieved the string that way. You may also pass in the string directly. 

```
with open('C:\\path\\to\\creds\\of_email.json') as f:
    data = json.load(f)


mdb = MailDB(data.get('user'),data.get("password"))

```

Example of credentials file: 

```
{
  "user":"mail_user_name",
  "password":"mail_password"
}   
```

You may also call the MailDB() class without any user and password arguments if you supply a path to a JSON file containing the credentials. The default path is ~/.maildb/creds.json 

```
mdb = MailDB()
```

### How to use

Below is an example of how to insert a document to the "database".
```
mdb = MailDB(data.get('user'),data.get("password"))
insert_key ="key_one"
insert_value = { "key": "value" }
mdb.insert(key=insert_key,value=insert_value)

```

Below is an example of how to get a document from the "database" using a key.

```
raw_data = mdb.get(key=insert_key)

# raw_data = {"key":"value"}
```

Below is an example of how to update an existing key from the "database".

```
insert_key ="key_one"

update_value = {
    "new":"value",
    "test":123
}
print (mdb.update(key=insert_key,value=update_value))

```

The update function will fail if no such key exist, unless you pass in the forced_insert boolean to True.
```
insert_key ="key_two"

update_value = {
    "new":"value",
    "test":123
}
print (mdb.update(key=insert_key,value=update_value,forced_insert=True))

```

The deletion function will allow you to delete entries in the database by key.

```
mdb.delete(key=insert_key)
```
## Libraries used

* smtplib - Used for sending mail
* imaplib - Used for getting mail



## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgements

As comical as it may be, I like to list out the amount of stackoverflows that I used to come up with this project as I go along. 

```
https://stackoverflow.com/questions/6209616/get-email-subject-and-sender-using-imaplib
https://stackoverflow.com/questions/703185/using-email-headerparser-with-imaplib-fetch-in-python
https://stackoverflow.com/questions/14080629/python-3-imaplib-fetch-typeerror-cant-concat-bytes-to-int
https://stackoverflow.com/questions/25235010/how-to-get-the-body-text-of-email-with-imaplib
https://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail/642988#642988
https://stackoverflow.com/questions/19540192/imap-get-sender-name-and-body-text
https://stackoverflow.com/questions/2230037/how-to-fetch-an-email-body-using-imaplib-in-python
https://stackoverflow.com/questions/19001266/how-to-search-specific-e-mail-using-python-imaplib-imap4-search
https://stackoverflow.com/questions/25186394/unable-to-retrieve-gmail-messages-from-any-folder-other-than-inbox-python3-issu
https://stackoverflow.com/questions/27743728/python-imaplib-fetch-result-is-none-with-simple-email-from-gmail
https://stackoverflow.com/questions/13403790/python-imap-search-for-partial-subject
https://stackoverflow.com/questions/7314942/python-imaplib-to-get-gmail-inbox-subjects-titles-and-sender-name
https://stackoverflow.com/questions/17872094/python-how-to-parse-things-such-as-from-to-body-from-a-raw-email-source-w
```
