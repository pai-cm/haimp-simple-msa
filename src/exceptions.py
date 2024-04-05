class HaimpException(Exception):
    message: str

    def __int__(self, message: str):
        self.message = message


class DatabaseException(HaimpException):
    """데이터 베이스에서 발생한 Exception"""
