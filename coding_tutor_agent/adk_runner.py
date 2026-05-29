#!/usr/bin/env python3

from pathlib import Path
from .agent import root_agent
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner

DB_URL = Path(__file__).parent / "adk_sessions.db"
session_service = DatabaseSessionService(
    db_url=f"sqlite+aiosqlite:///{DB_URL}"
)

APP_NAME = "BodeTutor"

runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service
    )
