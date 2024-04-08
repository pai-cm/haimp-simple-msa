from fastapi import APIRouter, Depends

from src.users.login_manager import LoginManager
from webapp.dependency import login_manager_dependency
from webapp.dto import SignupRequestDTO, OkDTO, LoginRequestDTO, TokenDTO, RefreshTokenDTO

router = APIRouter()


@router.post("/users/sign-up")
async def sign_up(
  request_body: SignupRequestDTO,
  login_manager: LoginManager = Depends(login_manager_dependency)
) -> OkDTO:
    await login_manager.sign_up(request_body.to_domain(), request_body.password)

    return OkDTO(ok=True)


@router.post("/users/token")
async def login(
    request_body: LoginRequestDTO,
    login_manager: LoginManager = Depends(login_manager_dependency)
) -> TokenDTO:
    token = await login_manager.login(request_body.to_domain())
    return TokenDTO.from_domain(token)


@router.post("/users/refresh")
async def refresh_token(
    request_body: RefreshTokenDTO,
    login_manager: LoginManager = Depends(login_manager_dependency)
) -> TokenDTO:
    token = await login_manager.refresh(request_body.refresh_token)
    return TokenDTO.from_domain(token)
