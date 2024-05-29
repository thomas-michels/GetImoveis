from fastapi import APIRouter, Depends, Query, Security
from fastapi.exceptions import HTTPException
from app.api.composers import user_composer
from app.api.dependencies.authenticate import user_authentication
from app.api.shared_schemas.user import CreateUser
from app.core.entities import UserInDB
from app.core.services import UserServices

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("")
async def create_user(
    create_user: CreateUser, services: UserServices = Depends(user_composer)
):
    user_in_db = await services.create(create_user=create_user)

    if not user_in_db:
        raise HTTPException(status_code=400, detail="Some error happen")

    return user_in_db


@router.get("/email")
async def get_user_by_email(
    email: str = Query(),
    services: UserServices = Depends(user_composer),
    user_authentication: UserInDB = Security(user_authentication, scopes="")
):
    user_in_db = await services.get_by_email(email=email)

    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found!")

    return user_in_db


@router.get("/me")
async def get_current_user(
    user_authentication: UserInDB = Security(user_authentication, scopes="")
):
    return user_authentication
