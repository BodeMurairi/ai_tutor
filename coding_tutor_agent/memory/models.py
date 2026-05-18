#!/usr/bin/env python3

import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from ..schema.user import SkillLevel
from ..schema.session import Intent


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    skill_level: Mapped[SkillLevel] = mapped_column(Enum(SkillLevel), default=SkillLevel.beginner)
    preferred_language: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    language_used: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    sessions: Mapped[list["SessionModel"]] = relationship("SessionModel", back_populates="user")


class SessionModel(Base):
    __tablename__ = "sessions"

    session_id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    current_language: Mapped[str] = mapped_column(String, nullable=False)
    current_intent: Mapped[Intent] = mapped_column(Enum(Intent), nullable=False)
    current_topic: Mapped[str] = mapped_column(String, nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="sessions")
