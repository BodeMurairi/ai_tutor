#!/usr/bin/env python3

import os

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", 24))

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or ""

CHAT_RATE_LIMIT = "5/hour"
