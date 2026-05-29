#!/usr/bin/env python3

import os
import smtplib
import asyncio
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def _send(recipient_email: str, first_name: str, api_key: str) -> None:
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = (os.getenv("SMTP_PASSWORD") or "").replace(" ", "")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your NexVecta AI Tutor API Key"
    msg["From"] = smtp_user
    msg["To"] = recipient_email

    plain = MIMEText(
        f"Hi {first_name},\n\nHere is your API key:\n\n{api_key}\n\n"
        "Keep it safe — treat it like a password.\n\nNexVecta Team",
        "plain"
    )
    html = MIMEText(f"""\
<!DOCTYPE html>
<html>
  <body style="font-family:sans-serif;max-width:480px;margin:auto;padding:24px">
    <h2>Welcome, {first_name}!</h2>
    <p>Your NexVecta AI Tutor account is ready. Here is your API key:</p>
    <pre style="background:#f4f4f4;padding:12px;border-radius:6px;font-size:14px">{api_key}</pre>
    <p style="color:#666;font-size:12px">Keep this key safe — treat it like a password. Do not share it.</p>
    <p>— The NexVecta Team</p>
  </body>
</html>""", "html")

    msg.attach(plain)
    msg.attach(html)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, recipient_email, msg.as_string())


async def send_api_key_email(recipient_email: str, first_name: str, api_key: str) -> None:
    """Send the generated API key to the newly registered user."""
    await asyncio.to_thread(_send, recipient_email, first_name, api_key)
