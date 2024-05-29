import re
from pydantic import BaseModel, Field, EmailStr, SecretStr
from passlib.context import CryptContext
from datetime import datetime
from app.core.exceptions.user_exceptions import InvalidPassword, UnprocessableEntity


_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
_PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()\-=_+{};:\'"\\|,.<>?]).+$'


class User(BaseModel):
    first_name: str = Field(example="First")
    last_name: str = Field(example="Last Name")
    email: EmailStr = Field(example="email@test.com")
    password: SecretStr = Field(exclude=True)

    def validate_password(self, password: str, repeat_password: str) -> None:
        errors = []

        if password != repeat_password:
            raise UnprocessableEntity(message="As senhas precisam ser iguais!")

        if len(password) < 8:
            errors.append("A senha deve conter no mínimo 8 caracteres!")
        
        if len(password) > 24:
            errors.append("O tamanho máximo para a senha é de 24 caracteres!")

        if not re.match(_PASSWORD_REGEX, password):
            errors.append("A senha deve ter pelo menos um caracter especial e letras maiusculas e minusculas!")

        if errors:
            raise InvalidPassword(message=" ".join(errors))

    def get_encripted_password(self) -> str:
        return _pwd_context.hash(self.password.get_secret_value())


class UserInDB(User):
    id: int = Field(example=123)
    created_at: datetime = Field(example=str(datetime.now()))
    updated_at: datetime = Field(example=str(datetime.now()))

    def verify_password(self, password: str) -> bool:
        if password:
            return _pwd_context.verify(password, self.password.get_secret_value())

        else:
            return False
