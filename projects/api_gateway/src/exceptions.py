class HaimpException(Exception):
    message: str

    def __init__(self, message: str):
        self.message = message


class ExpiredTokenException(HaimpException):
    """만료된 토큰"""


class InvalidSignatureException(HaimpException):
    """토큰 검증 실패"""
