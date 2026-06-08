#!/usr/bin/env python3

from uuid import uuid4
from google.genai.types import Content, Part

from ..adk_runner import runner, session_service, APP_NAME
from ..memory.database import AsyncSessionLocal
from ..memory.repository import get_registration_by_username, get_username
from ..memory.models import UserModel
from ..schema.session import ChatRequest, ChatResponse


async def _get_or_create_user_state(username: str) -> dict:
    """
    Load user data from DB and return as session state dict.
    Creates a UserModel profile if one doesn't exist yet.
    Returns the state dict and the real user_id for ADK.
    """
    async with AsyncSessionLocal() as db:
        registration = await get_registration_by_username(db, username)
        if not registration:
            return {"username": username, "first_name": username, "user_id": None}

        profile = await get_username(db, username)
        if not profile:
            profile = UserModel(
                user_id=registration.id,
                name=f"{registration.first_name} {registration.last_name}",
                username=registration.username,
            )
            db.add(profile)
            await db.commit()
            await db.refresh(profile)

    return {
        "username": username,
        "first_name": registration.first_name,
        "api_key": registration.api_key,
        "user_id": profile.id,
        "last_summary": "",
        "message_count": 0,
        "should_summarize": False,
    }


async def handle_chat(request: ChatRequest, username: str) -> ChatResponse:
    """Handle a chat request for an authenticated user."""
    session_id = request.session_id or str(uuid4())

    state = await _get_or_create_user_state(username)
    adk_user_id = state["user_id"] or username

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=adk_user_id,
        session_id=session_id
    )

    if not session:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=adk_user_id,
            session_id=session_id,
            state=state
        )

    import logging
    logger = logging.getLogger(__name__)

    response_text = ""
    async for event in runner.run_async(
        user_id=adk_user_id,
        session_id=session_id,
        new_message=Content(role="user", parts=[Part.from_text(text=request.message)])
    ):
        logger.info(f"[event] is_final={event.is_final_response()} has_content={event.content is not None}")
        if event.is_final_response() and event.content and event.content.parts:
            text = "".join(
                part.text for part in event.content.parts if hasattr(part, "text") and part.text
            )
            logger.info(f"[event] final response text length={len(text)}")
            if text:
                response_text = text

    return ChatResponse(response=response_text, session_id=session_id)
