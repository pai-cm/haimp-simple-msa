import pytest

from src.domains import User, LoginRequest


@pytest.fixture
def given_user():
    user = User(
        name="pai-cm",
        role="admin",
        group="haimp"
    )
    yield user


@pytest.fixture
async def given_login_request(given_user, given_repository):
    user = given_user
    password = "1234"
    await given_repository.create_user(user, password)
    yield LoginRequest(user.name, password)


async def test_user_reader(given_user_reader, given_login_request, given_user):
    user_reader = given_user_reader
    user_domain = await user_reader.read_by_login_request(given_login_request)

    assert user_domain == given_user


