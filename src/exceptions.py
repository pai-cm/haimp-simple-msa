class HaimpException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message


class DatabaseException(HaimpException):
    """데이터 베이스에서 발생한 Exception"""


class InvalidTokenException(HaimpException):
    """"""


class InvalidUserException(HaimpException):
    """유저 정보가 잘못 되었을 때"""


class NotFoundException(DatabaseException):
    """데이터를 찾지 못했을 때"""


class DBIntegrityException(DatabaseException):
    """"""


class AlreadySignUpException(DatabaseException):
    """이미 등록된 계정"""


class ExpiredTokenException(HaimpException):
    """만료된 토큰"""


class InvalidRequestException(HaimpException):
    """ 부적절한 요청 왔을 때"""