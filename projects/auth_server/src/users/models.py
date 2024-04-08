from sqlalchemy import Column, String

from src.database import Base
from src.domains import User


class UserEntity(Base):

    __tablename__ = "users"

    user_name = Column(String, primary_key=True)
    password = Column(String, nullable=True)

    user_group = Column(String, nullable=True)
    user_role = Column(String, nullable=True)

    @staticmethod
    def new(user: User, password: str):
        return UserEntity(
            user_name=user.name,
            password=password,
            user_group=user.group,
            user_role=user.role
        )

    def to_domain(self) -> User:
        return User(
            name=self.user_name,
            role=self.user_role,
            group=self.user_group,
        )
