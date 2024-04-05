import pytest

from src.exceptions import InvalidRequestException
from webapp.dto import SignupRequestDTO


def test_create_SignupRequestBody():
    given_request_body = {
        "username": "pai-cm",
        "password": "12asvaskbnklasd34",
        "user_role": "admin",
        "user_group": "haimp-developer"
    }

    dto = SignupRequestDTO(**given_request_body)

    assert dto.username == 'pai-cm'
    assert dto.password == '12asvaskbnklasd34'
    assert dto.user_role == 'admin'
    assert dto.user_group == 'haimp-developer'


def test_convert_to_dict_SignupRequestBody():
    given_dto = SignupRequestDTO(
        username='pai-cm',
        password='12asvaskbnklasd34',
        user_role='admin',
        user_group='haimp-developer'
    )

    data = given_dto.dict()

    assert data["username"] == 'pai-cm'
    assert data["password"] == '12asvaskbnklasd34'
    assert data["user_role"] == 'admin'
    assert data["user_group"] == 'haimp-developer'


def test_raise_exception_when_password_is_not_valid():
    with pytest.raises(InvalidRequestException):
        SignupRequestDTO(
            username='pai-cm',
            password='12a34',
            user_role='admin',
            user_group='haimp-developer'
        )
