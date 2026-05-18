#!/usr/bin/env python3

from google.adk.tools.tool_context import ToolContext
from ..memory.database import AsyncSessionLocal
from ..memory.repository import create_user, get_user_by_name
from ..schema.user import User, SkillLevel


async def save_user(
    name: str,
    tool_context: ToolContext,
    skill_level: str = "beginner",
    preferred_language: str | None = None
) -> dict:
    """
    Save a new user to the database. If the user already exists, return their data.
    Call this tool as soon as the user provides their name.
    """
    async with AsyncSessionLocal() as session:
        existing = await get_user_by_name(session, name)
        if existing:
            user_dict = User.model_validate(existing, from_attributes=True).model_dump(mode="json")
        else:
            user_data = User(
                name=name,
                skill_level=SkillLevel(skill_level),
                preferred_language=preferred_language
            )
            new_user = await create_user(session, user_data)
            user_dict = User.model_validate(new_user, from_attributes=True).model_dump(mode="json")

    tool_context.state["user_id"] = user_dict["id"]
    tool_context.state["username"] = user_dict["username"]
    return user_dict


async def update_session_tool(
    current_language: str,
    current_intent: str,
    current_topic: str,
    tool_context: ToolContext
) -> dict:
    """
    Update the session context with the current programming language, intent, and topic.
    Call this tool once the language, intent, and topic are identified from the conversation.
    """
    tool_context.state["current_language"] = current_language
    tool_context.state["current_intent"] = current_intent
    tool_context.state["current_topic"] = current_topic
    return {"status": True, "message": "Session context updated"}
