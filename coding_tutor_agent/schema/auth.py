#!/usr/bin/env python3

import uuid
from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import List, Optional

class Login(BaseModel):
    """Authenticate as an user"""
    username: Optional[str] = Field(default=None, description="User name")
    email_address: Optional[EmailStr] = Field(default=None, description="User email address")
    api_key: str = Field(..., description="User api key")

class GenerateKey(BaseModel):
    """Regenerate key"""
    username:str = Field(description="Username")
    email_address:EmailStr = Field(description="User email address") 

class NewKey(BaseModel):
    """generate and send key"""
    email_address:EmailStr = Field(description="User email address")
    api_key:str = Field(default_factory=lambda:str(uuid.uuid4()),description="User API Key")

class JWT_KEY(BaseModel):
    username:str = Field(description="User name from the db")
    jwt:str = Field(description="JWT Code")
