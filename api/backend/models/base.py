# ruff: noqa

from sqlalchemy import URL
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
)
from fastapi import Depends

from backend.configs import Configs

# Sync
# engine: Engine = create_engine(Configs.PG_URI)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Core
async def get_connection(db_url=Configs.PG_URI) -> AsyncEngine:
    engine: AsyncEngine = create_async_engine(db_url)
    return engine


# ORM
async def get_session(engine: AsyncEngine = Depends(create_async_engine)):
    async_session: AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return async_session
