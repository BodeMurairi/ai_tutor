#!/usr/bin/env python3

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..memory.database import get_session
from ..memory.models import UserRegistration

bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    session: AsyncSession = Depends(get_session),
) -> str:
    api_key = credentials.credentials
    result = await session.execute(
        select(UserRegistration).where(UserRegistration.api_key == api_key)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return user.username
