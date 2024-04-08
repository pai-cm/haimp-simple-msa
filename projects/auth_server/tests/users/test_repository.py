import pytest

from src.domains import User, LoginRequest
from src.exceptions import DatabaseException


async def test_create_user_and_read_by_login_request(given_repository):
    user = User(
        name="pai-cm",
        role="admin",
        group="haimp"
    )

    await given_repository.create_user(user, "123")

    result = await given_repository.read_by_login_request(LoginRequest("pai-cm", "123"))

    assert user == result


async def test_create_user_and_try_to_read_by_wrong_login_request(given_repository):
    user = User(
        name="pai-cm",
        role="admin",
        group="haimp"
    )

    await given_repository.create_user(user, "123")

    with pytest.raises(DatabaseException):
        await given_repository.read_by_login_request(LoginRequest("pai-cm", "1234"))


async def test_create_user_and_read_by_user_name(given_repository):
    user = User(
        name="pai-cm",
        role="admin",
        group="haimp",
    )

    await given_repository.create_user(user, "123")

    result = await given_repository.read_by_user_name(user.name)

    assert user == result
