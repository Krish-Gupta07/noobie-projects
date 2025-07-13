from imap_tools.mailbox import MailBox
import os
from dotenv import load_dotenv


load_dotenv()

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
if not MAIL_USERNAME:
    print("ERROR: MAIL_USERNAME not found in .env file")
    exit(1)

MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
if not MAIL_PASSWORD:
    print("ERROR: MAIL_PASSWORD not found in .env file")
    exit(1)

imap_list = []

def imap(MAIL_USERNAME, MAIL_PASSWORD):
 with MailBox("imap.gmail.com").login(MAIL_USERNAME, MAIL_PASSWORD, "Inbox") as mb:
    global imap_list
    # print(mb.folder.list())
    for msg in mb.fetch(limit=5, reverse=True, mark_seen=True):
        response = [msg.subject, msg.date, msg.text]
        imap_list.append(response)
 return imap_list

def get_emails():
    imap(MAIL_USERNAME, MAIL_PASSWORD)
    return imap_list


imap(MAIL_USERNAME, MAIL_PASSWORD)
