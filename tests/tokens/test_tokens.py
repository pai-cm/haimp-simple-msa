import pytest

from src.domains import TokenType, User
from src.exceptions import ExpiredTokenException
from src.tokens.manager import create_jwt_token
import jwt


def test_create_jwt_token_access(given_private_pem, given_public_pem):
    # given
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp"
    }

    # when
    access_token = create_jwt_token(given_payload, TokenType.ACCESS, given_private_pem, 10)

    payload = jwt.decode(access_token, given_public_pem, algorithms=['RS256'])

    # then
    assert payload['type'] == "access"
    assert payload['user_name'] == "pai-cm"


def test_create_jwt_token_expired_case(given_private_pem, given_public_pem):
    # given
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp"
    }

    # when
    access_token = create_jwt_token(given_payload, TokenType.ACCESS, given_private_pem, -10)

    with pytest.raises(jwt.exceptions.ExpiredSignatureError):
        jwt.decode(access_token, given_public_pem, algorithms=['RS256'])


def test_create_jwt_token_refresh(given_private_pem, given_public_pem):
    # given
    given_payload = {
    }

    # when
    refresh_token = create_jwt_token(given_payload, TokenType.REFRESH, given_private_pem, 10)

    payload = jwt.decode(refresh_token, given_public_pem, algorithms=['RS256'])

    # then
    assert payload['type'] == "refresh"


def test_generate_token(given_private_pem, given_public_pem, given_token_manager):
    # user
    user = User(
        name="pai-cm",
        role="admin",
        group="haimp"
    )

    token = given_token_manager.generate_token(user)
    output = jwt.decode(token.access, given_public_pem, algorithms=['RS256'])

    assert user.to_dict()["user_name"] == output["user_name"]
    
    
def test_verify_refresh_token(given_token_manager):
    # user
    user = User(
        name="pai-cm",
        role="admin",
        group="haimp"
    )

    token = given_token_manager.generate_token(user)
    user_name = given_token_manager.verify_refresh_token(token.refresh)

    assert user_name == user.name


def test_verify_refresh_token_with_expired(given_token_manager, given_private_pem):
    # given
    given_payload = {
        "user_name": "pai-cm"
    }

    # when
    refresh_token = create_jwt_token(given_payload, TokenType.REFRESH, given_private_pem, -10)

    with pytest.raises(ExpiredTokenException):
        given_token_manager.verify_refresh_token(refresh_token)
