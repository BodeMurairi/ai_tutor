#!/usr/bin/env python3

from ..services.chat import handle_chat
from ..schema.session import ChatRequest, ChatResponse


async def chat(request: ChatRequest, username: str) -> ChatResponse:
    return await handle_chat(request=request, username=username)
