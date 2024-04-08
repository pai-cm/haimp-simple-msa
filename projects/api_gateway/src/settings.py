from pydantic_settings import BaseSettings
from pydantic import Field


class ApiGatewaySettings(BaseSettings):
    """ Api Gateway를 위한 환경 변수 목록들 """
    public_key: bytes = Field(
        description='Public Pem Contents'
    )
