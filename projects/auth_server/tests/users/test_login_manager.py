import jwt
import pytest

from src.domains import User, LoginRequest, TokenType
from src.exceptions import DatabaseException


@pytest.fixture
def given_user():
    user = User(
        name="pai-cm",
        role="admin",
        group="haimp"
    )
    yield user


@pytest.fixture
def given_password():
    yield "1234"


@pytest.fixture
async def given_login_request(given_user, given_password, given_repository):
    user = given_user
    password = given_password
    await given_repository.create_user(user, password)
    yield LoginRequest(user.name, password)


async def test_sign_up(given_user, given_password, given_login_manager, given_repository):
    await given_login_manager.sign_up(given_user, given_password)

    user = await given_repository.read_by_user_name(given_user.name)

    assert given_user == user


async def test_sign_up_duplicate_raise_error(given_user, given_password, given_login_manager, given_repository):
    await given_login_manager.sign_up(given_user, given_password)

    with pytest.raises(DatabaseException):
        await given_login_manager.sign_up(given_user, given_password)


async def test_login(given_login_manager, given_login_request, given_public_pem):
    token = await given_login_manager.login(given_login_request)

    access_payload = jwt.decode(token.access, given_public_pem, algorithms=['RS256'])
    refresh_payload = jwt.decode(token.refresh, given_public_pem, algorithms=['RS256'])

    assert access_payload["type"] == TokenType.ACCESS.value
    assert access_payload["user_name"] == given_login_request.username

    assert refresh_payload["type"] == TokenType.REFRESH.value


async def test_try_to_login_with_wrong_password(given_login_manager, given_login_request):
    given_login_request.password += "123"

    with pytest.raises(DatabaseException):
        await given_login_manager.login(given_login_request)


async def test_refresh_token(given_repository, given_password, given_login_manager, given_token_manager):
    # user
    user = User(
        name="pai-cm",
        role="admin",
        group="haimp"
    )

    await given_repository.create_user(user, given_password)

    expired_token = given_token_manager.generate_token(user)
    new_token = await given_login_manager.refresh(expired_token.refresh)

    assert expired_token.access != new_token.access
    assert expired_token.refresh != new_token.refresh
