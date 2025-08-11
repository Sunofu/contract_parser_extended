# email_reader.py
import os
import imaplib
import email
from email.header import decode_header
import re


def fetch_attachments(imap_host, login, password, save_dir="temp_files"):
    os.makedirs(save_dir, exist_ok=True)
    with imaplib.IMAP4_SSL(imap_host) as imap:
        imap.login(login, password)
        imap.select("inbox")
        status, messages = imap.search(None, '(UNSEEN)')
        attachments = []
        for num in messages[0].split()[:1000]:
            print(f"Смотрит письмо {num}")
            _, msg_data = imap.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get("Content-Disposition") is None:
                    continue
                filename = part.get_filename()
                if filename:
                    filename = decode_and_sanitize_filename(filename)
                    filepath = os.path.join(save_dir, filename)
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    attachments.append(filepath)
        return attachments


def decode_and_sanitize_filename(filename: str):
    # Декодируем MIME-заголовок
    decoded_parts = decode_header(filename)
    decoded_str = ""
    for part, enc in decoded_parts:
        if isinstance(part, bytes):
            decoded_str += part.decode(enc or "utf-8", errors="ignore")
        else:
            decoded_str += part

    # Убираем переносы строк и запрещённые символы
    decoded_str = decoded_str.replace("\r", "").replace("\n", "")
    decoded_str = re.sub(r'[\\/*?:"<>|]', "_", decoded_str)
    return decoded_str
