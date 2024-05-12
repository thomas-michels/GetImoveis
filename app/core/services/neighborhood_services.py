from app.core.db.repositories import NeighborhoodRepository
from app.core.entities import Neighborhood, NeighborhoodInDB


class NeighborhoodServices:
    def __init__(self, neighborhood_repository: NeighborhoodRepository) -> None:
        self.__neighborhood_repository = neighborhood_repository

    async def create(self, neighborhood: Neighborhood) -> NeighborhoodInDB:
        neighborhood_in_db = await self.__neighborhood_repository.insert(
            neighborhood=neighborhood
        )
        return neighborhood_in_db
