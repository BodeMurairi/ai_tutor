#!/usr/bin/env python3

import uuid
from pydantic import BaseModel, Field, EmailStr


class GenerateKey(BaseModel):
    """Identity verification to reset a lost API key"""
    username: str = Field(description="Username")
    email_address: EmailStr = Field(description="User email address")


class NewKey(BaseModel):
    """generate and send key"""
    email_address: EmailStr = Field(description="User email address")
    api_key: str = Field(default_factory=lambda: str(uuid.uuid4()), description="User API Key")
