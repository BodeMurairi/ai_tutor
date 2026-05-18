#!/usr/bin/env python3

import logging
from google.adk.agents.callback_context import CallbackContext
from google.genai import types

from .memory.database import AsyncSessionLocal
from .memory.repository import create_session, update_session
from .schema.session import Session, Intent

logger = logging.getLogger(__name__)


async def after_agent_callback(callback_context: CallbackContext) -> types.Content | None:
    """
    Runs after each subagent response. Reads session context from state
    and persists it to the database.
    """
    user_id = callback_context.state.get("user_id")
    username = callback_context.state.get("username")
    current_language = callback_context.state.get("current_language")
    current_intent = callback_context.state.get("current_intent")
    current_topic = callback_context.state.get("current_topic")

    logger.info(f"[callback] state → user_id={user_id}, username={username}, "
                f"language={current_language}, intent={current_intent}, topic={current_topic}")

    if not all([user_id, username, current_language, current_intent, current_topic]):
        logger.warning("[callback] Missing state values — session not saved.")
        return None

    try:
        session_id = callback_context._invocation_context.session.id
    except AttributeError:
        logger.error("[callback] Could not retrieve session_id.")
        return None

    try:
        intent = Intent(current_intent)
    except ValueError:
        logger.warning(f"[callback] Unknown intent '{current_intent}', defaulting to 'learning'.")
        intent = Intent.learning

    try:
        async with AsyncSessionLocal() as db:
            result = await update_session(
                db,
                session_id=session_id,
                current_language=current_language,
                current_intent=intent.value,
                current_topic=current_topic
            )
            if not result["status"]:
                session_data = Session(
                    session_id=session_id,
                    user_id=user_id,
                    username=username,
                    current_language=current_language,
                    current_intent=intent,
                    current_topic=current_topic
                )
                await create_session(db, session_data)
                logger.info(f"[callback] New session created → {session_id}")
            else:
                logger.info(f"[callback] Session updated → {session_id}")
    except Exception as e:
        logger.error(f"[callback] DB error: {e}")

    return None
