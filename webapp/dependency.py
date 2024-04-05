from fastapi import Depends

from src.database import Database
from src.settings import AuthSettings
from src.tokens import TokenManager
from src.users.login_manager import LoginManager
from src.users.repository import UserRepository


def settings_dependency():
    return AuthSettings()


def database_dependency(settings=Depends(settings_dependency)):
    return Database(settings)


def user_repository_dependency(database=Depends(database_dependency)):
    return UserRepository(database.session)

def token_manager_dependency(settings=Depends(settings_dependency)):
    return TokenManager(settings)

def login_manager_dependency(repository=Depends(user_repository_dependency), token_manager=Depends(token_manager_dependency)):
    return LoginManager(repository, token_manager)