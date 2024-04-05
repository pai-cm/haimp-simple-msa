from pydantic import BaseModel, Field, field_validator
from src.domains import User, LoginRequest
from src.exceptions import InvalidRequestException


class SignupRequestDTO(BaseModel):
    username: str = Field(description="유저 이름")
    password: str = Field(description="유저의 비밀번호")
    user_role: str = Field(description="유저가 소속한 그룹에서의 역할")
    user_group: str = Field(description="유저가 소속한 그룹")

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
    ok: bool = Field(description="성공ㄴ")


class LoginRequestDTO(BaseModel):
    username: str = Field()
    password: str = Field()

    def to_domain(self):
        return LoginRequest(
            username=self.username,
            password=self.password
        )


class TokenDTO(BaseModel):
    access_token: str = Field()
    refresh_token: str = Field()


class RefreshTokenDTO(BaseModel):
    refresh_token: str = Field()