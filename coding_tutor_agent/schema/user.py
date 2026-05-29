#!/usr/bin/env python3

import uuid
from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserRegistration(BaseModel):
    """User registration model"""
    model_config = ConfigDict(from_attributes=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="User ID auto generated during registration")
    first_name:str = Field(..., description="User first name")
    last_name:str = Field(..., description="User last name")
    username:str = Field(..., description="Username as saved in the db")
    email_address:EmailStr = Field(..., description="User email address")
    api_key:str = Field(default_factory=lambda:f"pkey-{str(uuid.uuid4())}")

class SkillLevel(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class User(BaseModel):
    """User profile model"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="User id")
    skill_level: SkillLevel = Field(default=SkillLevel.beginner, description="User skill level")
    preferred_language: Optional[str] = Field(default=None, description="Preferred programming language")
    language_used: List[str] = Field(default_factory=list, description="Languages used across conversations")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
