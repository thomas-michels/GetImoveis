from fastapi import Depends
from fastapi.security import SecurityScopes
from app.api.dependencies.user_authentication import (
    UserAuthentication,
    UserToken
)
from app.api.composers import user_composer
from app.api.shared_schemas.jwt_schemas import ApiJWT

JWT_TOKEN_HEADER = "Authorization"


async def user_authentication(
        security_scopes: SecurityScopes,
        user_services = Depends(user_composer),
        jwt_token: str = Depends(UserToken(name=JWT_TOKEN_HEADER, description="Authenticate users"), use_cache=False)
    ) -> ApiJWT:
    user_auth = UserAuthentication(services=user_services, scopes_needed=security_scopes)

    return await user_auth(jwt_token)
