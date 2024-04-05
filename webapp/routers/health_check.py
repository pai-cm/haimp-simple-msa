from fastapi import APIRouter

from webapp.dto import OkDTO

router = APIRouter()


@router.get("/")
def health_check() -> OkDTO:
    return OkDTO(ok=True)