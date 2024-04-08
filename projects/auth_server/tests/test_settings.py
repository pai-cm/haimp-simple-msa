from src.settings import AuthSettings
import os


def test_initialize_auth_settings(given_private_pem):
    settings = AuthSettings(
        db_type="sqlite+aiosqlite:///file.db",
        private_key=given_private_pem,
        access_token_lifetime=10000,
        refresh_token_lifetime=86400
    )

    assert settings.db_type == "sqlite+aiosqlite:///file.db"
    assert settings.private_key == given_private_pem
    assert settings.access_token_lifetime == 10000
    assert settings.refresh_token_lifetime == 86400


def test_initialize_auth_settings_from_env(given_private_pem):
    os.environ['db_host'] = "sqlite+aiosqlite:///file.db"
    os.environ['private_key'] = given_private_pem.decode('utf-8')
    os.environ['access_token_lifetime'] = '10000'
    os.environ['refresh_token_lifetime'] = '86400'

    settings = AuthSettings()

    assert settings.db_type == "sqlite+aiosqlite:///file.db"
    assert settings.private_key == given_private_pem
    assert settings.access_token_lifetime == 10000
    assert settings.refresh_token_lifetime == 86400


def test_initialize_auth_settings_from_env_upper(given_private_pem):
    os.environ['DB_HOST'] = "sqlite+aiosqlite:///file.db"
    os.environ['PRIVATE_KEY'] = given_private_pem.decode('utf-8')
    os.environ['ACCESS_TOKEN_LIFETIME'] = '10000'
    os.environ['REFRESH_TOKEN_LIFETIME'] = '86400'

    settings = AuthSettings()

    assert settings.db_type == "sqlite+aiosqlite:///file.db"
    assert settings.private_key == given_private_pem
    assert settings.access_token_lifetime == 10000
    assert settings.refresh_token_lifetime == 86400

