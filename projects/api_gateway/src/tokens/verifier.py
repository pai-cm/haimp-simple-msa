import jwt

from projects.api_gateway.src.exceptions import ExpiredTokenException, InvalidSignatureException


class TokenVerifier:
    """
    토큰 검증
    """
    def __init__(self, public_key):
        self.public_key = public_key

    def verify_access_token(self, access_token: str):
        """access token을 검증합니다."""

        # public_key 로 access token 을 검증합니다.
        try:
            payload = jwt.decode(access_token, self.public_key, algorithms=['RS256'])
            return payload

        except jwt.exceptions.ExpiredSignatureError:
            raise ExpiredTokenException("만료된 토큰 입니다")

        except jwt.exceptions.InvalidSignatureError:
            raise InvalidSignatureException("검증 실패 토큰 입니다")
