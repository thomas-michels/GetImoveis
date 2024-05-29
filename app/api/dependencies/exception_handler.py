from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def generic_validation(request: Request, exc):

    if hasattr(exc, "message"):
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder({"message": exc.message}),
        )

    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({"message": "Internal error"}),
    )
