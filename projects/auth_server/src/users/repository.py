from contextlib import AbstractContextManager
from typing import Callable

import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from src.domains import LoginRequest, User
from src.exceptions import DatabaseException
from src.users.models import UserEntity


class UserRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def create_user(self, user: User, password: str):
        async with self.session_factory() as session:
            user_entity = UserEntity.new(user, password)
            session.add(user_entity)
            await session.commit()

    async def read_by_user_name(self, user_name: str) -> User:
        """ 유저 이름으로 유저 객체를 조회해오는 로직 """
        async with self.session_factory() as session:
            stmt = select(UserEntity).where(
                and_(
                    UserEntity.user_name == user_name
                )
            )
            try:
                entity: UserEntity = (await session.execute(stmt)).scalars().one()
                return entity.to_domain()
            except sqlalchemy.exc.NoResultFound:
                raise DatabaseException("데이터가 발견되지 않았습니다.")

    async def read_by_login_request(self, login_request: LoginRequest) -> User:
        async with self.session_factory() as session:
            statement = select(UserEntity).where(
                and_(
                    UserEntity.user_name == login_request.username,
                    UserEntity.password == login_request.password,
                )
            )
            try:
                entity: UserEntity = (await session.execute(statement)).scalars().one()
                return entity.to_domain()
            except sqlalchemy.exc.NoResultFound:
                raise DatabaseException("데이터가 발견되지 않았습니다.")
