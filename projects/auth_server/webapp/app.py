from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from projects.auth_server.webapp.routers import auth, health_check


def create_app() -> FastAPI:
    app = FastAPI(
        title="Haimp Auth Server",
        description="Haimp 내 계정계를 관리합니다."
    )

    app.include_router(
        auth.router,
        tags=['authentication']
    )

    app.include_router(
        health_check.router,
        tags=['health-check'],
        include_in_schema=False
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app