from dataclasses import dataclass
from enum import Enum
from typing import Dict

from src.exceptions import InvalidTokenException, InvalidUserException

"""
로그인 기능
Id, password 로 로그인 함수를 통하면 access token 과 refresh token 이 나온다
id, password로 유저 정보 조회 하면 유저 정보가 나오고 user 정보로 token 생성,하면 access token 과 refresh token 나온다
"""


@dataclass
class LoginRequest:
    """ 로그인에 필요한 필수 정보"""
    user_name: str
    password: str


@dataclass
class User:
    """유저 정보"""
    name: str
    role: str
    group: str

    def to_dict(self):
        """dict 변환"""
        return {
            "user_name": self.name,
            "user_role": self.role,
            "user_group": self.group
        }

    @staticmethod
    def from_dict(data: Dict):
        try:
            return User(
                name=data['user_name'],
                role=data['user_role'],
                group=data['user_group']
            )
        except KeyError as e:
            raise InvalidUserException(f"유저에 대한 필수 필드가 누락되었습니다. {e}")


@dataclass
class Token:
    """JWT Token 객체"""
    access: str
    refresh: str


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

    @staticmethod
    def from_text(text: str) -> 'TokenType':
        for token_type in TokenType:
            if token_type.value.lower().strip() == text.lower().strip():
                return token_type
        raise InvalidTokenException("유효하지 않은 토큰 타입입니다.")
