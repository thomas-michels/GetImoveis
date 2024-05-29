from pydantic import BaseModel, Field, EmailStr


class SignIn(BaseModel):
    email: EmailStr = Field(example="email@test.com")
    password: str = Field(example="Test@2024")
