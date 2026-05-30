#!/usr/bin/env python3
import smtplib
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(Path("coding_tutor_agent/.env"), override=True)

user = os.getenv("SMTP_USER")
password = os.getenv("SMTP_PASSWORD") or ""

print(f"User   : {user}")
print(f"Pw len : {len(password)}")
print(f"Pw     : {password}")   # remove after confirming

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.ehlo()
        s.starttls()
        s.login(user, password)
        print("Login successful!")
except Exception as e:
    print(f"Error: {e}")
