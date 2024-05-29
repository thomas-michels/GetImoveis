
from datetime import datetime, timedelta
from typing import Dict
import jwt
from pydantic import ValidationError
from app.api.shared_schemas.jwt_schemas import ApiJWT, JWTMeta


JWT_SUBJECT = "access"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 36  # one week


def create_jwt_token(
        jwt_content: Dict[str, str],
        secret_key: str,
        expires_delta: timedelta,
) -> str:
    to_encode = jwt_content.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update(JWTMeta(exp=expire, sub=JWT_SUBJECT).model_dump())
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)


def create_access_token(
        user_id: int,
        secret_key: str
    ) -> str:

    return create_jwt_token(
        jwt_content=ApiJWT(
            user_id=user_id,
        ).model_dump(),
        secret_key=secret_key,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def decode_jwt(secret_key: str, token: str) -> ApiJWT:
    try:
        api_jwt = ApiJWT(**jwt.decode(token, secret_key, algorithms=[ALGORITHM]))
        return api_jwt

    except jwt.PyJWTError as decode_error:
        raise ValueError("unable to decode JWT token") from decode_error

    except ValidationError as validation_error:
        raise ValueError("malformed payload in token") from validation_error
