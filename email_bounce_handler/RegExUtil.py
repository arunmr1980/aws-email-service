import re

def get_email_ids(message):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_regex_obj = re.compile(email_regex)
    matched_emails = email_regex_obj.findall(message)
    return matched_emails


# msg = "The following identities failed the check in region US-EAST-2: strider.galaxie@gmail.com, merry.aru@gmail.com"
# print (get_email_ids(msg))
