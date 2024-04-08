from dataclasses import dataclass
from typing import Annotated, Optional

from fastapi import APIRouter, Depends

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from starlette.responses import Response

from src.tokens.verifier import TokenVerifier
from webapp.dependency import token_verifier_dependency
from dataclasses import asdict
import httpx

router = APIRouter()

security = HTTPBearer(auto_error=False)


@dataclass
class UserInfo:
    user_name: str
    user_role: str
    user_group: str

    def to_dict(self):
        return asdict(self)


async def dependency_user_info(
        credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
        token_verifier: TokenVerifier = Depends(token_verifier_dependency)
) -> Optional[UserInfo]:
    if credentials is None:
        return None
    data = token_verifier.verify_access_token(credentials.credentials)
    try:
        return UserInfo(
            user_name=data['user_name'],
            user_role=data['user_role'],
            user_group=data['user_group']
        )
    except KeyError as e:
        raise ValueError("필수 정보가 누락되어 있습니다.")


@router.api_route("/{host_server}/{path:path}",
                  methods=["GET", "POST", "PUT", "DELETE", "HEAD"])
async def api_gateway(
        host_server: str,
        path: str,
        request: Request,
        user_info: Optional[UserInfo] = Depends(dependency_user_info)
):
    headers = request.headers.mutablecopy()

    for key in headers.keys():
        if key.startswith('x-haimp-'):
            del headers[key]
        if key == 'authorization':
            del headers[key]

    if user_info:
        headers = {
            **headers,
            "x-haimp-user-name": user_info.user_name,
            "x-haimp-user-role": user_info.user_role,
            "x-haimp-user-group": user_info.user_group
        }

    async with httpx.AsyncClient() as client:
        data = await client.request(request.method,
                                    f'http://{host_server}/{path}',
                                    params=request.query_params,
                                    content=await request.body(),
                                    headers=headers)
        return Response(
            data.content,
            status_code=data.status_code,
            headers=data.headers
        )
