from fastapi import APIRouter

from webapp.dto import SignupRequestDTO, OkDTO, LoginRequestDTO, TokenDTO, RefreshTokenDTO

router = APIRouter()


@router.post("/users/sign-up")
def sign_up(
  request_body: SignupRequestDTO
) -> OkDTO:
    pass


@router.post("/users/token")
def login(
    request_body: LoginRequestDTO
) -> TokenDTO:
    pass

@router.post("/users/refresh")
def refresh_token(
    request_body: RefreshTokenDTO
) -> TokenDTO:
    pass
