#!/usr/bin/env python3

import uuid
import logging

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..schema.user import UserRegistration as UserSchema
from ..schema.auth import GenerateKey
from ..memory.models import UserRegistration
from .email import send_api_key_email

logger = logging.getLogger(__name__)


class AuthenticationService:

    def __init__(self, session: AsyncSession):
        self.session = session

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

    async def reset_api_key(self, data) -> dict:
        result = await self.session.execute(
            select(UserRegistration).where(
                UserRegistration.username == data.username,
                UserRegistration.email_address == data.email_address,
            )
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        new_key = f"pkey-{uuid.uuid4()}"
        user.api_key = new_key
        await self.session.commit()
        await self.session.refresh(user)

        try:
            await send_api_key_email(user.email_address, user.first_name, new_key)
        except Exception as e:
            logger.warning("Failed to send new API key email to %s: %s", user.email_address, e)

        return {"status": "success", "api_key": new_key}
