#!/usr/bin/env python3

from uuid import uuid4
from google.genai.types import Content, Part

from ..adk_runner import runner, session_service, APP_NAME
from ..memory.database import AsyncSessionLocal
from ..memory.repository import get_registration_by_username
from ..schema.session import ChatRequest, ChatResponse


async def handle_chat(request: ChatRequest, username: str) -> ChatResponse:
    """This function handles chat"""
    session_id = request.session_id or str(uuid4())
    user_id = session_id

    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )

    if not session:
        async with AsyncSessionLocal() as db:
            registration = await get_registration_by_username(db, username)
        first_name = registration.first_name if registration else username
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
            state={"username": username, "first_name": first_name}
        )

    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=Content(role="user", parts=[Part.from_text(text=request.message)])
    ):
        if event.is_final_response() and event.content and event.content.parts:
            response_text = event.content.parts[0].text

    return ChatResponse(response=response_text, session_id=session_id)
