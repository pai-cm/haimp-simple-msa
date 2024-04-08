from datetime import datetime

import pytest

import jwt

from projects.api_gateway.src.exceptions import InvalidSignatureException, ExpiredTokenException


def test_token_encode_decode(given_private_pem, given_public_pem):
    # given
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp"
    }

    # when
    access_token = jwt.encode(given_payload, given_private_pem, algorithm='RS256')

    payload = jwt.decode(access_token, given_public_pem, algorithms=['RS256'])

    # then
    assert payload['user_name'] == "pai-cm"


def test_token_invalid_signature_error(given_private_pem, given_public_pem):
    # 탈취당한 access token
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJwYWktY20iLCJ1c2VyX3JvbGUiOiJhZG1pbiIsInVzZXJfZ3JvdXAiOiJoYWltcCJ9.f9iUMXGY6bPMh5cSbwuPn3ydJ06fYSUKJgj9Npp0zF4VDPX86wXuone9fHbnN47QzOVeqmZIMOF0o409tlrTHhF0nN81ef2brQg5-UiRKIVAql_wRH2WoVzDWGLayaWH6cmzt5KUAkEzWRzfrO9XC6y8j_0yiRcm7uSKYKzi6W4"

    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        jwt.decode(access_token, given_public_pem, algorithms=['RS256'])


def test_token_verifier(given_private_pem, given_public_pem, given_token_verifier):
    # given
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp"
    }

    # when
    access_token = jwt.encode(given_payload, given_private_pem, algorithm='RS256')

    payload = given_token_verifier.verify_access_token(access_token)

    assert payload['user_name'] == "pai-cm"
    assert payload["user_role"] == "admin"
    assert payload["user_group"] == "haimp"


def test_token_verifier_invalid_error(given_private_pem, given_public_pem, given_token_verifier):
    access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJwYWktY20iLCJ1c2VyX3JvbGUiOiJhZG1pbiIsInVzZXJfZ3JvdXAiOiJoYWltcCJ9.f9iUMXGY6bPMh5cSbwuPn3ydJ06fYSUKJgj9Npp0zF4VDPX86wXuone9fHbnN47QzOVeqmZIMOF0o409tlrTHhF0nN81ef2brQg5-UiRKIVAql_wRH2WoVzDWGLayaWH6cmzt5KUAkEzWRzfrO9XC6y8j_0yiRcm7uSKYKzi6W4"

    with pytest.raises(InvalidSignatureException):
        given_token_verifier.verify_access_token(access_token)


def test_token_verifier_expired_error(given_private_pem, given_public_pem, given_token_verifier):
    # given
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp",
        "exp": datetime.now().timestamp() - 10,
    }

    # when
    access_token = jwt.encode(given_payload, given_private_pem, algorithm='RS256')

    with pytest.raises(ExpiredTokenException):
        given_token_verifier.verify_access_token(access_token)
