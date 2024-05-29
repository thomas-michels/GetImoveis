from pydantic import BaseModel, Field, EmailStr


class CreateUser(BaseModel):
    first_name: str = Field(example="First")
    last_name: str = Field(example="Last Name")
    email: EmailStr = Field(example="email@test.com")
    password: str = Field(example="Test@2024")
    confirm_password: str = Field(example="Test@2024")
