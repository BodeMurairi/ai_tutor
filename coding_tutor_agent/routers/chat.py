#!/usr/bin/env python3

from fastapi import Depends, Request
from fastapi.routing import APIRouter

from ..controllers.chat import chat
from ..schema.session import ChatRequest, ChatResponse
from ..services.dependencies import get_current_user
from ..services.rate_limiter import limiter
from ..config.config import CHAT_RATE_LIMIT

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
@limiter.limit(CHAT_RATE_LIMIT)
async def chat_endpoint(
    request: Request,
    body: ChatRequest,
    username: str = Depends(get_current_user)
):
    return await chat(request=body, username=username)
