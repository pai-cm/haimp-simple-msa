from pydantic_settings import BaseSettings
from pydantic import Field


class AuthSettings(BaseSettings):
    """ Auth Server를 위한 환경 변수 목록들 """
    db_host: str = Field(
        description="DB HOST",
        default='sqlite+aiosqlite:///:memory:'
    )

    private_key: bytes = Field(
        description='Private Pem Contents'
    )

    access_token_lifetime: int = Field(
        description="Access Token 수명(단위 초)",
        default=86400, # 하루
    )

    refresh_token_lifetime: int = Field(
        description="Refresh Token 수명(단위 초)",
        default=2592000, # 한달
    )

