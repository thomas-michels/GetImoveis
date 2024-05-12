from fastapi import FastAPI
from app.core.db import lifespan
from starlette.middleware.cors import CORSMiddleware
from app.api.routes import address_router, neighborhood_router, property_router


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

    app.include_router(address_router)
    app.include_router(neighborhood_router)
    app.include_router(property_router)

    return app
