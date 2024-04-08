from fastapi import Depends

from src.settings import ApiGatewaySettings
from src.tokens.verifier import TokenVerifier


def settings_dependency():
    return ApiGatewaySettings()


def token_verifier_dependency(settings=Depends(settings_dependency)):
    return TokenVerifier(settings)
