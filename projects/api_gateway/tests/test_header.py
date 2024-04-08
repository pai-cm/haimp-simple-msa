import json
from unittest.mock import patch, AsyncMock

import pytest
from httpx import AsyncClient, Response
from starlette.requests import QueryParams
import jwt
from functools import partial


AsyncClient = partial(AsyncClient, base_url="http://api-server")


@pytest.mark.asyncio
async def test_get_header_access_token(test_app):
    test_host_server = "api-server"
    test_path = "data-server"

    async with AsyncClient(app=test_app) as ac:
        with pytest.raises(jwt.exceptions.DecodeError):
            await ac.get(f"/{test_host_server}/{test_path}",
                         headers={"Authorization": "Bearer abcdef12345"})


@pytest.mark.asyncio
async def test_get_header_access_token_fail(test_app):
    test_host_server = "data-server"
    test_path = "images/32"

    async with AsyncClient(app=test_app) as ac:
        response = await ac.get(f"/{test_host_server}/{test_path}")

        assert response.json() == 'fail'


@pytest.mark.asyncio
async def test_get_header_payload(given_private_pem, test_app):
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp"
    }

    access_token = jwt.encode(given_payload, given_private_pem, algorithm='RS256')

    test_host_server = "data-server"
    test_path = "images/32"

    async with AsyncClient(app=test_app) as ac:
        response = await ac.get(f"/{test_host_server}/{test_path}", headers={"Authorization": f"Bearer {access_token}"})

        payload = response.json()

        assert response.status_code == 200
        assert given_payload["user_name"] == payload["user_name"]


@pytest.mark.asyncio
async def test_post_with_request_body(given_private_pem, test_app):
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp"
    }

    given_body = {
        "key": "hello",
        "data": "world"
    }

    access_token = jwt.encode(given_payload, given_private_pem, algorithm='RS256')

    test_host_server = "data-server"
    test_path = "data/register"

    with patch('httpx.AsyncClient') as mock_client:
        mock_request = AsyncMock()

        mock_client.return_value.__aenter__.return_value.request = mock_request
        mock_client.return_value.__aenter__.return_value.request.return_value = Response(200, content=b"hello")
        async with AsyncClient(app=test_app) as ac:
            response = await ac.post(
                f"/{test_host_server}/{test_path}",
                json=given_body,
                headers={"Authorization": f"Bearer {access_token}"}
            )

            mock_request.assert_called_with(
                "POST",
                "http://data-server/data/register",
                params=QueryParams(''),
                content=b'{"key": "hello", "data": "world"}',
                headers={
                    'host': 'api-server',
                    'accept': '*/*',
                    'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive',
                    'user-agent': 'python-httpx/0.27.0', 'content-length': '33', 'content-type': 'application/json',
                    'x-haimp-user-name': 'pai-cm', 'x-haimp-user-role': 'admin', 'x-haimp-user-group': 'haimp'}
            )

            assert response.status_code == 200
            assert response.content == b'hello'


@pytest.mark.asyncio
async def test_get_with_request_query_param(given_private_pem, test_app):
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp"
    }

    access_token = jwt.encode(given_payload, given_private_pem, algorithm='RS256')

    test_host_server = "data-server"
    test_path = "data/register"

    with patch('httpx.AsyncClient') as mock_client:
        mock_request = AsyncMock()

        mock_client.return_value.__aenter__.return_value.request = mock_request
        mock_client.return_value.__aenter__.return_value.request.return_value = Response(200)
        async with AsyncClient(app=test_app) as ac:
            response = await ac.get(
                f"/{test_host_server}/{test_path}?order=seq&skill=python",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            mock_request.assert_called_with(
                "GET",
                "http://data-server/data/register",
                params=QueryParams('order=seq&skill=python'),
                content=b'',
                headers={'host': 'api-server', 'accept': '*/*',
                         'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive',
                         'user-agent': 'python-httpx/0.27.0', 'x-haimp-user-name': 'pai-cm',
                         'x-haimp-user-role': 'admin', 'x-haimp-user-group': 'haimp'}
            )

            assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_with_request(given_private_pem, test_app):
    given_payload = {
        "user_name": "pai-cm",
        "user_role": "admin",
        "user_group": "haimp"
    }

    access_token = jwt.encode(given_payload, given_private_pem, algorithm='RS256')

    test_host_server = "data-server"
    test_path = "data/register"

    with patch('httpx.AsyncClient') as mock_client:
        mock_request = AsyncMock()

        mock_client.return_value.__aenter__.return_value.request = mock_request
        mock_client.return_value.__aenter__.return_value.request.return_value = Response(200)
        async with AsyncClient(app=test_app) as ac:
            response = await ac.delete(
                f"/{test_host_server}/{test_path}?order=seq&skill=python",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            mock_request.assert_called_with(
                "DELETE",
                "http://data-server/data/register",
                params=QueryParams('order=seq&skill=python'),
                content=b'',
                headers={'host': 'api-server', 'accept': '*/*',
                         'accept-encoding': 'gzip, deflate', 'connection': 'keep-alive',
                         'user-agent': 'python-httpx/0.27.0', 'x-haimp-user-name': 'pai-cm',
                         'x-haimp-user-role': 'admin', 'x-haimp-user-group': 'haimp'}
            )

            assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_delete_with_expired(given_private_pem, test_app):
#     given_payload = {
#         "user_name": "pai-cm",
#         "user_role": "admin",
#         "user_group": "haimp",
#         "exp": 0
#     }
#
#     access_token = jwt.encode(given_payload, given_private_pem, algorithm='RS256')
#
#     test_host_server = "data-server"
#     test_path = "data/register"
#
#     with patch('httpx.AsyncClient') as mock_client:
#         mock_request = AsyncMock()
#
#         mock_client.return_value.__aenter__.return_value.request = mock_request
#         mock_client.return_value.__aenter__.return_value.request.return_value = Response(200)
#         async with AsyncClient(app=test_app) as ac:
#             response = await ac.delete(
#                 f"/{test_host_server}/{test_path}?order=seq&skill=python",
#                 headers={"Authorization": f"Bearer {access_token}"}
#             )
#
#             data = response.json()
#
#             assert response.status_code == 401
#             assert data['code'] == 'ExpiredTokenException'
