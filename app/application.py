from fastapi import FastAPI
from app.core.db import lifespan
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import (
    address_router,
    neighborhood_router,
    property_router,
    user_router,
    user_auth_router
)
from app.api.dependencies.exception_handler import generic_validation


def create_app() -> FastAPI:
    app = FastAPI(
        title="Get Imoveis",
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(user_auth_router)
    app.include_router(user_router)
    app.include_router(address_router)
    app.include_router(neighborhood_router)
    app.include_router(property_router)

    app.add_exception_handler(Exception, generic_validation)

    return app
