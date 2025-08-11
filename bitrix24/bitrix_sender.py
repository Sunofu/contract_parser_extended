# bitrix24/bitrix_sender.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BITRIX_WEBHOOK = os.getenv("BITRIX_WEBHOOK")

def send_to_bitrix24(title, description):
    url = f"{BITRIX_WEBHOOK}/crm.lead.add.json"
    data = {
        "fields": {
            "TITLE": title,
            "COMMENTS": description
        }
    }
    r = requests.post(url, json=data)
    return r.json()
