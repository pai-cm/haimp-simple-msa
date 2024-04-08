from src.domains import User, LoginRequest, Token
from src.exceptions import DBIntegrityException, AlreadySignUpException
from src.tokens.manager import TokenManager
from src.users.repository import UserRepository


class LoginManager:
    def __init__(self, user_repository: UserRepository, token_manager: TokenManager):
        self.user_repository = user_repository
        self.token_manager = token_manager

    async def sign_up(self, user: User, password: str):
        """
        유저 객체와 비밀번호를 받으면
        """
        try:
            await self.user_repository.create_user(user, password)
        except DBIntegrityException:
            raise AlreadySignUpException("이미 가입된 유저입니다.")

    async def login(self, login_request: LoginRequest) -> Token:
        """
        유저
        토큰을 반환합니다.
        """
        user = await self.user_repository.read_by_login_request(login_request)
        return self.token_manager.generate_token(user=user)
    
    async def refresh(self, refresh_token: str) -> Token:
        # refresh token의 만료 여부를 확인합니다
        # token 에서 user_name 을 반환합니다
        user_name = self.token_manager.verify_refresh_token(refresh_token)

        # user 객체를 반환합니다
        user = await self.user_repository.read_by_user_name(user_name)

        # token 을 생성하여 반환합니다.
        return self.token_manager.generate_token(user)
