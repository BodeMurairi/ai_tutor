#!/usr/bin/env python3

import logging
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..memory.database import get_session
from ..memory.models import UserRegistration

logger = logging.getLogger(__name__)
bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    session: AsyncSession = Depends(get_session),
) -> str:
    api_key = credentials.credentials
    logger.info(f"[auth] Authorization header received — Bearer {api_key[:8]}...{api_key[-4:]}")
    result = await session.execute(
        select(UserRegistration).where(UserRegistration.api_key == api_key)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    #logger.info(f"[auth] API key validated — user: {user.username}")
    return user.username
