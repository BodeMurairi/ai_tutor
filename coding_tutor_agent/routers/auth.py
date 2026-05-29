#!/usr/bin/env python3

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from ..schema.user import UserRegistration as User
from ..schema.auth import Login, GenerateKey
from ..memory.database import get_session
from ..controllers.auth import register_user, login_user, reset_api_key

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(user: User, session: AsyncSession = Depends(get_session)):
    return await register_user(user=user, session=session)


@router.post("/login")
async def login(credentials: Login, session: AsyncSession = Depends(get_session)):
    return await login_user(credentials=credentials, session=session)


@router.post("/reset-key")
async def reset_key(data: GenerateKey, session: AsyncSession = Depends(get_session)):
    return await reset_api_key(data=data, session=session)
