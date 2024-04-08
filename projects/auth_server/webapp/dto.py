from pydantic import BaseModel, Field, field_validator
from src.domains import User, LoginRequest, Token
from src.exceptions import InvalidRequestException


class SignupRequestDTO(BaseModel):
    username: str = Field(description="유저 이름", examples=["pai-cm"])
    password: str = Field(description="유저의 비밀번호", examples=["password1234"])
    user_role: str = Field(description="유저가 소속한 그룹에서의 역할", examples=["admin"])
    user_group: str = Field(description="유저가 소속한 그룹", examples=['haimp-developer'])


    @field_validator('password')
    @classmethod
    def password_must_contain_both(cls, v):
        # 최소 10자 이상인지 확인
        if len(v) < 8:
            raise InvalidRequestException('최소 10글자 이상 해주세요')

        # 영어와 숫자가 각각 하나 이상 포함되어 있는지 확인
        has_alpha = any(char.isalpha() for char in v)
        has_digit = any(char.isdigit() for char in v)

        if not (has_alpha and has_digit):
            raise InvalidRequestException('Password에는 최소 한글자 이상의 영어와 숫자가 포함되어야 합니다.')

        return v

    def to_domain(self):
        return User(
            name=self.username,
            role=self.user_role,
            group=self.user_group
        )


class OkDTO(BaseModel):
    ok: bool = Field(description="성공")


class LoginRequestDTO(BaseModel):
    username: str = Field(examples=["pai-cm"])
    password: str = Field(examples=["password1234"])

    def to_domain(self):
        return LoginRequest(
            username=self.username,
            password=self.password
        )


class TokenDTO(BaseModel):
    access_token: str = Field(examples=["eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTIzMzM0NDUuNjQ2NTksInVzZXJuYW1lIjoicGFpLWNtIiwidXNlcmdyb3VwIjoiaGFpbXAtZGV2ZWxvcGVyIiwicm9sZSI6ImFkbWluIn0.PVtjQ90hOnkANGpV1SNrKEnrw8PyU64MBmz3-0hGXdIpZR2eUbn7G4cRyF5Ez2SMXQhf6hRs5eBxvuB2y-9QNm7fDbR7xdRDQUbmCjbxlpBCYKNBhQFxP2xCvXcQ6_5nW0IMuTU0iEfEKfxmoerkXBY7ieD-wcGuKiMg7eYyqt4"])
    refresh_token: str = Field(examples=["eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTIzMzM0NjcuNTQ3ODcsInVzZXJuYW1lIjoicGFpLWNtIiwidXNlcmdyb3VwIjoiaGFpbXAtZGV2ZWxvcGVyIiwicm9sZSI6ImFkbWluIn0.SIUOSWoAqjqLMaADbg3nqqQBxzoC9dKCwkforhr5hhtOddecX0bgvc9l83AwfbOsADDlh9kKOV5CzibeR1TEgoRxKm6jWOaZ94prdEgs4BH54QnaJ_iDNaFczyMgkgi-ELrLsBFqvD2njqgH3VnQgmSa6LkYEAWB6WAL0dC4WUw"])

    @staticmethod
    def from_domain(domain:Token):
        return TokenDTO(
            access_token=domain.access,
            refresh_token=domain.refresh
        )


class RefreshTokenDTO(BaseModel):
    refresh_token: str = Field(examples=["eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTIzMzM0NjcuNTQ3ODcsInVzZXJuYW1lIjoicGFpLWNtIiwidXNlcmdyb3VwIjoiaGFpbXAtZGV2ZWxvcGVyIiwicm9sZSI6ImFkbWluIn0.SIUOSWoAqjqLMaADbg3nqqQBxzoC9dKCwkforhr5hhtOddecX0bgvc9l83AwfbOsADDlh9kKOV5CzibeR1TEgoRxKm6jWOaZ94prdEgs4BH54QnaJ_iDNaFczyMgkgi-ELrLsBFqvD2njqgH3VnQgmSa6LkYEAWB6WAL0dC4WUw"])