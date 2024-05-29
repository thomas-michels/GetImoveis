from pydantic import BaseModel, Field
from datetime import datetime


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class ApiJWT(BaseModel):
    user_id: int = Field(example=123)
