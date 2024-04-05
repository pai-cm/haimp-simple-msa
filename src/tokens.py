from typing import Dict

import jwt

from src.auth import private_pem2public_pem
from src.domains import User, Token, TokenType

from datetime import datetime

from src.exceptions import ExpiredTokenException
from src.users.repository import UserRepository


class TokenManager:

    def __init__(
            self,
            user_repository: UserRepository,
            private_key: bytes,
            access_token_lifetime: int = 86400,  # 하루
            refresh_token_lifetime: int = 2592000,  # 한달
    ):
        self.user_repository = user_repository
        self.private_key = private_key
        self.access_token_lifetime = access_token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime

    def generate_token(self, user: User) -> Token:
        """access token 을 생성합니다."""

        # access token 만들기
        access = create_jwt_token(
            user.to_dict(),
            TokenType.ACCESS,
            self.private_key,
            self.access_token_lifetime
        )

        # refresh token 만들기
        refresh = create_jwt_token(
            {"user_name": user.name}, TokenType.REFRESH, self.private_key, self.refresh_token_lifetime
        )

        return Token(access=access, refresh=refresh)

    def verify_refresh_token(self, refresh_token: str) -> str:
        public_key = private_pem2public_pem(self.private_key)
        try:
            output = jwt.decode(refresh_token, public_key, algorithms=['RS256'])
            return output["user_name"]
        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException("만료된 토큰 입니다")


def create_jwt_token(
        payload: Dict,
        type: TokenType,
        private_key: bytes,
        lifetime: int
) -> str:
    """JWT 토큰을 생성합니다"""
    update_payload = {
        **payload,
        "type": type.value,
        "exp": datetime.now().timestamp() + lifetime,
    }

    jwt_token = jwt.encode(update_payload, private_key, algorithm='RS256')

    return jwt_token
