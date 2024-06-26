"""Database module."""
import asyncio
from contextlib import AbstractContextManager, asynccontextmanager
from typing import Callable
import logging

import sqlalchemy.exc
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session
from src.exceptions import DatabaseException, NotFoundException, DBIntegrityException
from src.settings import AuthSettings

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    """비동기 데이터베이스 클래스"""

    def __init__(self, settings: AuthSettings):
        if settings.db_type.startswith('sqlite'):
            self._engine = create_async_engine(settings.db_type)
        elif settings.db_type.startswith("postgresql"):
            url = f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
            self._engine = create_async_engine(url)
        else:
            raise DatabaseException(f"지원하지 않는 database type입니다. {settings.db_type}")

        self._session_factory = async_scoped_session(
            async_sessionmaker(
                autocommit=False,
                bind=self._engine,
            ),
            scopefunc=asyncio.current_task,
        )

    async def create_database(self) -> None:
        if self._engine.url.drivername != "sqlite+aiosqlite":
            raise ValueError("create_database should be used for test mode only.")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_database(self) -> None:
        if self._engine.url.drivername != "sqlite+aiosqlite":
            raise ValueError("drop_database should be used for test mode only.")
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self) -> Callable[..., AbstractContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except sqlalchemy.exc.NoResultFound:
            await session.rollback()
            raise NotFoundException("데이터를 못발견했아요")
        except sqlalchemy.exc.IntegrityError:
            await session.rollback()
            raise DBIntegrityException("데이터를 못발견했아요")


        except Exception as e:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise DatabaseException(f"DB 처리 중 문제가 발생했습니다. error: {e}")
        finally:
            await session.close()
            await self._session_factory.remove()

    async def connect(self):
        return await self._engine.connect()