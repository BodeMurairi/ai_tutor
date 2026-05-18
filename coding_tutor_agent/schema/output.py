#!/usr/bin/env python3

from typing import Optional, List
from pydantic import BaseModel, Field


class Output(BaseModel):
    """Structured output model for agent responses"""
    explanation: str = Field(..., description="Explanation provided to user")
    code_example: Optional[str] = Field(default=None, description="Code example provided to user")
    follow_up_questions: Optional[List[str]] = Field(default=None, description="Follow-up questions to check understanding")
    key_concepts: List[str] = Field(..., description="Concepts covered in this response")
