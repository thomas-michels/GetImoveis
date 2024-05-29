from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.api.composers import user_composer
from app.api.shared_schemas.signin import SignIn
from app.api.dependencies.jwt import create_access_token
from app.core.services import UserServices
from app.core.configs import get_environment

_env = get_environment()
router = APIRouter(prefix="", tags=["Auth"])


@router.post("/signin")
async def signin(
    signin: SignIn, services: UserServices = Depends(user_composer)
):
    user_in_db = await services.autenticate(signin=signin)

    if not user_in_db:
        raise HTTPException(status_code=401, detail="Email ou senha invalidos!")

    token = create_access_token(
        user_id=user_in_db.id,
        secret_key=_env.SECRET_KEY,
    )

    return token
