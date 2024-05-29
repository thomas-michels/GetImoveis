from app.core.db.repositories import (
    UserRepository
)
from app.core.entities import User, UserInDB
from app.api.shared_schemas.user import CreateUser
from app.api.shared_schemas.signin import SignIn


class UserServices:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.__user_repository = user_repository

    async def create(self, create_user: CreateUser) -> UserInDB:
        user = User(
            first_name=create_user.first_name,
            last_name=create_user.last_name,
            email=create_user.email,
            password=create_user.password
        )

        user.validate_password(
            password=create_user.password,
            repeat_password=create_user.confirm_password
        )

        user_in_db = await self.__user_repository.insert(user=user)

        return user_in_db

    async def get_by_email(self, email: str) -> UserInDB:
        user_in_db = await self.__user_repository.select_by_email(email=email)

        return user_in_db

    async def get_by_id(self, user_id: int) -> UserInDB:
        user_in_db = await self.__user_repository.select_by_id(user_id=user_id)

        return user_in_db

    async def autenticate(self, signin: SignIn) -> UserInDB:
        user_in_db = await self.__user_repository.select_by_email(email=signin.email)

        if user_in_db and user_in_db.verify_password(password=signin.password):
            return user_in_db
