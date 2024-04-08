import pytest

from src.domains import User, TokenType
from src.exceptions import InvalidTokenException


def test_to_dict():
    user = User("pai-cm", "admin", "haimp-group")

    user_data = user.to_dict()

    assert user_data['user_name'] == "pai-cm"
    assert user_data['user_role'] == "admin"
    assert user_data['user_group'] == "haimp-group"


def test_from_dict():
    user = User.from_dict({
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp-group",
    })

    assert user.name == "pai-cm"
    assert user.role == "admin"
    assert user.group == "haimp-group"


def test_token_type_from_text():
    assert TokenType.from_text("access") == TokenType.ACCESS
    assert TokenType.from_text("ACCESS") == TokenType.ACCESS
    assert TokenType.from_text("refresh") == TokenType.REFRESH
    assert TokenType.from_text("REFRESH") == TokenType.REFRESH

    with pytest.raises(InvalidTokenException):
        TokenType.from_text("ase")
