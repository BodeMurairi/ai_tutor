#!/usr/bin/env python3

import os

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or ""

CHAT_RATE_LIMIT = "5/hour"
