#!/usr/bin/env python3

from fastapi.routing import APIRouter


router = APIRouter(
    prefix="/chat",
    tags=["Chat Router"]
    )

@router.post("/")
async def chat_router():
    """chat router"""
    pass
