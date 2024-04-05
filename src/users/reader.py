from src.domains import LoginRequest
from src.users.repository import UserRepository


class UserReader:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def read_by_login_request(self, login_request: LoginRequest):
        """
        login request 객체를 받으면
        유저의 정보를 반환합니다
        """
        return await self.repository.read_by_login_request(login_request)
