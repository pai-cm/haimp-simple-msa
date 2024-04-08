from urllib.request import Request

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.exceptions import HaimpException
from webapp.router import router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Haimp API gateway",
        description="Haimp 내 api gateway를 담당합니다."
    )

    app.include_router(
        router,
        tags=['api-gateway']
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(HaimpException)
    async def haimp_exception_handler(request: Request, exc: HaimpException):
        return JSONResponse(
            status_code=401,
            content={"message": exc.message, "code": exc.__class__.__name__},
        )

    return app
