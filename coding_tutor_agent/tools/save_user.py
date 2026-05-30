#!/usr/bin/env python3

from google.adk.tools.tool_context import ToolContext
from ..memory.database import AsyncSessionLocal
from ..memory.repository import get_registration_by_username, get_username
from ..memory.models import UserModel


async def load_user(tool_context: ToolContext) -> dict:
    """
    Load the authenticated user's data from the database into the session state.
    Call this tool at the start of every conversation before doing anything else.
    """
    username = tool_context.state.get("username")
    if not username:
        return {"status": "error", "message": "No authenticated user found in session."}

    async with AsyncSessionLocal() as session:
        registration = await get_registration_by_username(session, username)
        if not registration:
            return {"status": "error", "message": f"User '{username}' not found."}

        profile = await get_username(session, username)

        if not profile:
            profile = UserModel(
                user_id=registration.id,
                name=f"{registration.first_name} {registration.last_name}",
                username=registration.username,
            )
            session.add(profile)
            await session.commit()
            await session.refresh(profile)

    tool_context.state["user_id"] = profile.id
    tool_context.state["api_key"] = registration.api_key
    tool_context.state["first_name"] = registration.first_name

    return {
        "status": "success",
        "user_id": profile.id,
        "username": username,
        "first_name": registration.first_name,
        "api_key": registration.api_key,
    }


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
