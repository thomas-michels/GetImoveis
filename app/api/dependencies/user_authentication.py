from typing import Optional
from fastapi import Request
from fastapi.security import SecurityScopes, APIKeyHeader
from fastapi.exceptions import HTTPException
from app.core.services import UserServices
from app.core.entities import UserInDB
from app.api.dependencies.jwt import decode_jwt
from app.api.shared_schemas.jwt_schemas import ApiJWT
from app.core.configs import get_environment, get_logger

_env = get_environment()
logger = get_logger(__name__)


class UserToken(APIKeyHeader):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except HTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail="Token Invalido"
            )


class UserAuthentication:

    def __init__(self, services: UserServices, scopes_needed: SecurityScopes):
        self.scopes_needed = scopes_needed
        self.services = services

    async def __call__(self, token: str) -> UserInDB:
        try:
            api_jwt = decode_jwt(secret_key=_env.SECRET_KEY, token=token)

            if api_jwt:
                user_in_db = await self.services.get_by_id(user_id=api_jwt.user_id)

                # self.verify_scopes(user=user_in_db)

                return user_in_db

        except Exception as error:
            logger.error(f"Error on decode_jwt - Error: {str(error)}")

        raise HTTPException(status_code=401, detail="Credenciais invalidas!")

    # def verify_scopes(self, user: UserInDB) -> bool:
    #     checked_scopes = []

    #     for scope in self.scopes_needed.scopes:
    #         checked_scopes.append(user.role.check_has_permission(permission=scope))

    #     if not all(checked_scopes):
    #         raise HTTPException(
    #             status_code=403,
    #             detail="Access denied",
    #         )
