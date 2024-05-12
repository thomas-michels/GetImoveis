from fastapi import Depends
from app.core.services import NeighborhoodServices
from app.core.db import get_connection, DBConnection
from app.core.db.repositories import NeighborhoodRepository


async def neighborhood_composer(
    conn: DBConnection = Depends(get_connection),
) -> NeighborhoodServices:
    neighborhood_repository = NeighborhoodRepository(connection=conn)
    service = NeighborhoodServices(neighborhood_repository=neighborhood_repository)
    return service
