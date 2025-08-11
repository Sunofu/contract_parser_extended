# run_scheduled.py
import os
from email_reader import fetch_attachments
from main.handle_email_request import handle_email_request
from dotenv import load_dotenv

load_dotenv()

files = fetch_attachments(
    imap_host=os.getenv("EMAIL_HOST"),
    login=os.getenv("EMAIL_LOGIN"),
    password=os.getenv("EMAIL_PASSWORD")
)
if files:
    handle_email_request(files)
