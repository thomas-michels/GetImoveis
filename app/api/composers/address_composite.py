from fastapi import Depends
from app.core.services import AddressServices
from app.core.db import get_connection, DBConnection
from app.core.db.repositories import NeighborhoodRepository, StreetRepository, AddressRepository


async def address_composer(
    conn: DBConnection = Depends(get_connection),
) -> AddressServices:
    neighborhood_repository = NeighborhoodRepository(connection=conn)
    street_repository = StreetRepository(connection=conn)
    address_repository = AddressRepository(connection=conn)
    service = AddressServices(
        neighborhood_repository=neighborhood_repository,
        street_repository=street_repository,
        address_repository=address_repository
    )
    return service
