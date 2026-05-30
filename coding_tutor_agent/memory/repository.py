#!/usr/bin/env python3

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel, SessionModel, UserRegistration
from ..schema.user import User
from ..schema.session import Session


async def create_user(session: AsyncSession, user: User) -> UserModel:
    """Save a new user to the database"""
    new_user = UserModel(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def get_user_by_name(session: AsyncSession, name: str) -> UserModel | None:
    """Get a user by their name"""
    result = await session.execute(
        select(UserModel).where(UserModel.name == name)
    )
    return result.scalar_one_or_none()


async def get_registration_by_username(session: AsyncSession, username: str) -> UserRegistration | None:
    """Get a registered user by their username"""
    result = await session.execute(
        select(UserRegistration).where(UserRegistration.username == username)
    )
    return result.scalar_one_or_none()


async def get_username(session: AsyncSession, username: str) -> UserModel | None:
    """Get a user by their username"""
    result = await session.execute(
        select(UserModel).where(UserModel.username == username)
    )
    return result.scalar_one_or_none()


async def create_session(session: AsyncSession, session_data: Session) -> SessionModel:
    """Create a new conversation session"""
    new_session = SessionModel(**session_data.model_dump())
    session.add(new_session)
    await session.commit()
    await session.refresh(new_session)
    return new_session


async def get_last_session(session: AsyncSession, user_id: str) -> SessionModel | None:
    """Get the most recent session for a user"""
    result = await session.execute(
        select(SessionModel)
        .where(SessionModel.user_id == user_id)
        .order_by(desc(SessionModel.started_at))
        .limit(1)
    )
    return result.scalar_one_or_none()


async def update_session(session: AsyncSession, session_id: str, **kwargs) -> dict:
    """Update an existing session's fields"""
    result = await session.execute(
        select(SessionModel).where(SessionModel.session_id == session_id)
    )
    db_session = result.scalar_one_or_none()
    if db_session:
        for key, value in kwargs.items():
            setattr(db_session, key, value)
        await session.commit()
        return {"status": True}
    return {"status": False}
