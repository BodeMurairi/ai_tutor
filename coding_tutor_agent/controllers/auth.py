#!/usr/bin/env python3

from ..services.auth import AuthenticationService
from ..schema.user import UserRegistration as User
from ..schema.auth import Login, GenerateKey


async def register_user(user: User, session):
    service = AuthenticationService(session=session)
    return await service.register_user(user=user)


async def login_user(credentials: Login, session):
    service = AuthenticationService(session=session)
    return await service.login_user(credentials=credentials)


async def reset_api_key(data: GenerateKey, session):
    service = AuthenticationService(session=session)
    return await service.reset_api_key(data=data)
