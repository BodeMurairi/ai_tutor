#!/usr/bin/env python3

import os
import uuid
import logging
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from ..schema.user import UserRegistration as UserSchema
from ..schema.auth import Login, GenerateKey, JWT_KEY
from ..memory.models import UserRegistration
from .email import send_api_key_email

logger = logging.getLogger(__name__)


class AuthenticationService:

    def __init__(self, session: AsyncSession, username: str = None):
        self.session = session
        self.username = username

    def create_jwt(self) -> str:
        secret = os.getenv("JWT_SECRET", "change-me")
        expiry = int(os.getenv("JWT_EXPIRY_HOURS", 24))
        payload = {
            "sub": self.username,
            "exp": datetime.now(timezone.utc) + timedelta(hours=expiry),
        }
        return jwt.encode(
            payload, secret,
            algorithm="HS256"
            )

    async def register_user(self, user: UserSchema) -> dict:
        user.email_address = str(user.email_address)
        new_user = UserRegistration(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        email_sent = True
        try:
            await send_api_key_email(new_user.email_address, new_user.first_name, new_user.api_key)
        except Exception as error:
            logger.warning("Failed to send API key email to %s: %s", new_user.email_address, error)
            email_sent = False

        return {
            "status": "success",
            "email_sent": email_sent,
            "data": UserSchema.model_validate(new_user),
        }

    async def login_user(self, credentials: Login) -> JWT_KEY:
        conditions = []
        if credentials.username:
            conditions.append(UserRegistration.username == credentials.username)
        if credentials.email_address:
            conditions.append(UserRegistration.email_address == credentials.email_address)

        if not conditions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Provide a username or email address",
            )

        stmt = select(UserRegistration).where(or_(*conditions))
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or user.api_key != credentials.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        self.username = user.username
        return JWT_KEY(
            username=self.username,
            jwt=self.create_jwt()
            )

    async def reset_api_key(self, data: GenerateKey) -> dict:
        stmt = select(UserRegistration).where(
            UserRegistration.username == data.username,
            UserRegistration.email_address == data.email_address,
        )
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        new_key = f"pkey-{uuid.uuid4()}"
        user.api_key = new_key
        await self.session.commit()
        await self.session.refresh(user)

        try:
            await send_api_key_email(user.email_address, user.first_name, new_key)
        except Exception as e:
            logger.warning("Failed to send new API key email to %s: %s", user.email_address, e)

        return {
            "status": "success",
            "api_key": new_key
            }
