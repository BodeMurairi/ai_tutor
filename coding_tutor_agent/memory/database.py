#!/usr/bin/env python3

from pathlib import Path
from typing import AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base

DB_PATH = Path(__file__).parent.parent / "tutor.db"
db_url = f"sqlite+aiosqlite:///{DB_PATH}"

engine = create_async_engine(db_url, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def init_db_sync():
    sync_engine = create_engine(f"sqlite:///{DB_PATH}")
    Base.metadata.create_all(sync_engine)
    sync_engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
