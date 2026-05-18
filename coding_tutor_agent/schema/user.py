#!/usr/bin/env python3

import uuid
from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, model_validator


class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class User(BaseModel):
    """User profile model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="User id")
    name: str = Field(..., description="Full name as provided by the user")
    username: str = Field(default="", description="Username as saved in the system")
    skill_level: SkillLevel = Field(default=SkillLevel.beginner, description="User skill level")
    preferred_language: Optional[str] = Field(default=None, description="Preferred programming language")
    language_used: List[str] = Field(default_factory=list, description="Languages used across conversations")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @model_validator(mode="after")
    def set_username(self) -> "User":
        if not self.username:
            self.username = f"{self.name.lower().replace(' ', '_')}-{self.id[:8]}"
        return self
