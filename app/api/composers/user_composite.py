from fastapi import Depends
from app.core.services.user_services import UserServices
from app.core.db import get_connection, DBConnection
from app.core.db.repositories.user_repository import UserRepository


async def user_composer(
    conn: DBConnection = Depends(get_connection),
) -> UserServices:
    user_repository = UserRepository(connection=conn)
    service = UserServices(
        user_repository=user_repository
    )
    return service
