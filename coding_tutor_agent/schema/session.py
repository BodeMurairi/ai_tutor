#!/usr/bin/env python3

from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field


class Intent(str, Enum):
    learning = "learning"
    debugging = "debugging"
    exploring = "exploring"


class Session(BaseModel):
    """Conversation session state model"""
    session_id: str
    user_id: str = Field(..., description="User id")
    username: str = Field(..., description="Username for reference during conversation")
    current_language: str = Field(..., description="Programming language being discussed")
    current_intent: Intent = Field(..., description="User's current intent")
    current_topic: str = Field(..., description="Topic being explored")
    started_at: datetime = Field(default_factory=datetime.now, description="Session start time")
