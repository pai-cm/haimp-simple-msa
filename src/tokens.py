from typing import Dict

import jwt

from src.auth import load_pem
from src.domains import User, Token, TokenType

from datetime import datetime


class TokenGenerator:

    def __int__(self,
                pem_file: str,
                access_token_lifetime: int = 86400,  # 하루
                refresh_token_lifetime: int = 2592000,  # 한달
                ):
        self.private_key = load_pem(pem_file)
        self.access_token_lifetime = access_token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime

    def generate_token(self, user: User) -> Token:
        """access token 을 생성합니다."""

        # access token 만들기
        access = create_jwt_token(
            user.to_dict(),
            TokenType.ACCESS.value,
            self.private_key,
            self.access_token_lifetime
        )

        # refresh token 만들기
        refresh = create_jwt_token(
            {}, TokenType.REFRESH.value, self.private_key, self.refresh_token_lifetime
        )

        return Token(access=access, refresh=refresh)


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
