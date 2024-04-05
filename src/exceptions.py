class HaimpException(Exception):
    message: str

    def __int__(self, message: str):
        self.message = message


class DatabaseException(HaimpException):
    """데이터 베이스에서 발생한 Exception"""


class InvalidTokenException(HaimpException):
    """"""


class InvalidUserException(HaimpException):
    """유저 정보가 잘못 되었을 때"""
