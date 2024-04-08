import pytest
from Crypto.PublicKey import RSA
import tempfile
import os

from src.database import Database
from src.settings import AuthSettings
from src.tokens.manager import TokenManager
from src.users.login_manager import LoginManager
from src.users.repository import UserRepository


@pytest.fixture
def given_auth_settings(given_private_pem):
    yield AuthSettings(
        db_type="sqlite+aiosqlite:///:memory:",
        private_key=given_private_pem
    )


@pytest.fixture
async def given_database(given_auth_settings) -> Database:
    db = Database(given_auth_settings)
    await db.create_database()
    yield db
    await db.drop_database()


@pytest.fixture
def given_private_key():
    return RSA.generate(1024)


@pytest.fixture
def given_public_key(given_private_key):
    return given_private_key.public_key()


@pytest.fixture
def given_private_pem(given_private_key):
    return given_private_key.export_key()


@pytest.fixture
def given_public_pem(given_public_key):
    return given_public_key.export_key()


@pytest.fixture
def given_private_pem_file(given_private_key):
    fpath = tempfile.mktemp()
    with open(fpath, "wb") as f:
        f.write(given_private_key.export_key())
    yield fpath
    os.remove(fpath)


@pytest.fixture
def given_public_pem_file(given_public_key):
    fpath = tempfile.mktemp()
    with open(fpath, "wb") as f:
        f.write(given_public_key.export_key())
    yield fpath
    os.remove(fpath)


@pytest.fixture
def given_token_manager(given_auth_settings) -> TokenManager:
    return TokenManager(given_auth_settings)


@pytest.fixture
def given_repository(given_database):
    yield UserRepository(given_database.session)


@pytest.fixture
def given_user_reader(given_repository):
    yield UserReader(given_repository)


@pytest.fixture
def given_login_manager(given_repository, given_token_manager):
    yield LoginManager(given_repository, given_token_manager)
