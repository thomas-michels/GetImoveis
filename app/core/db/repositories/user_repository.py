from typing import List
from psycopg.errors import UniqueViolation
from app.core.db import DBConnection
from app.core.db.repositories.base_repository import Repository
from app.core.entities import User, UserInDB
from app.core.configs import get_logger
from app.core.exceptions.user_exceptions import UnprocessableEntity

_logger = get_logger(__name__)


class UserRepository(Repository):
    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    async def insert(self, user: User) -> UserInDB:
        try:
            query = """--sql
            INSERT INTO public.users
                (first_name, last_name, email, "password", created_at, updated_at, is_active)
                VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW(), true)
            RETURNING id, first_name, last_name, email, "password", created_at, updated_at;
            """

            raw_user = await self.conn.execute(
                sql_statement=query, values={
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "password": user.get_encripted_password(),
                }
            )

            if raw_user:
                return UserInDB(**raw_user)

        except UniqueViolation:
            raise UnprocessableEntity(message="Esse email já sendo utilizado, por favor utilize outro!")

        except Exception as error:
            _logger.error(f"Error: {str(error)}")

    async def select_by_email(self, email: str) -> UserInDB:
        try:
            query = """--sql
            SELECT
                id,
                first_name,
                last_name,
                email,
                "password",
                created_at,
                updated_at
            FROM
                public.users u
            WHERE
                u.email = %(email)s;
            """

            raw_user = await self.conn.execute(
                sql_statement=query, values={"email": email}
            )

            if raw_user:
                return UserInDB(**raw_user)

        except Exception as error:
            _logger.error(f"Error: {str(error)}")

    async def select_by_id(self, user_id: int) -> UserInDB:
        try:
            query = """--sql
            SELECT
                id,
                first_name,
                last_name,
                email,
                "password",
                created_at,
                updated_at
            FROM
                public.users u
            WHERE
                u.id = %(id)s;
            """

            raw_user = await self.conn.execute(
                sql_statement=query, values={"id": user_id}
            )

            if raw_user:
                return UserInDB(**raw_user)

        except Exception as error:
            _logger.error(f"Error: {str(error)}")
