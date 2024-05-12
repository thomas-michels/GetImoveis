from typing import List
from app.core.db.repositories import (
    NeighborhoodRepository,
    StreetRepository,
    AddressRepository,
)
from app.core.entities import Address, PlainAddress, Street, Neighborhood


class AddressServices:
    def __init__(
        self,
        neighborhood_repository: NeighborhoodRepository,
        street_repository: StreetRepository,
        address_repository: AddressRepository,
    ) -> None:
        self.__neighborhood_repository = neighborhood_repository
        self.__street_repository = street_repository
        self.__address_repository = address_repository

    async def create(self, address: Address) -> PlainAddress:
        neighborhood = await self.__neighborhood_repository.select_by_name(
            name=address.neighborhood
        )
        if not neighborhood:
            neighbor = Neighborhood(name=address.neighborhood)
            neighborhood = await self.__neighborhood_repository.insert(
                neighborhood=neighbor
            )

        street = await self.__street_repository.select_by_zip_code(
            zip_code=address.zip_code
        )
        if not street:
            street = await self.__street_repository.select_by_name(name=address.street)

        if not street:
            raw_street = Street(
                name=address.street,
                neighborhood_id=neighborhood.id,
                zip_code=address.zip_code,
                flood_quota=address.flood_quota,
                latitude=address.latitude,
                longitude=address.longitude,
            )
            street = await self.__street_repository.insert(street=raw_street)

        await self.__street_repository.conn.commit()

        return PlainAddress(
            street_id=street.id,
            street_name=street.name,
            neighborhood_id=neighborhood.id,
            neighborhood_name=neighborhood.name,
            zip_code=street.zip_code,
            flood_quota=street.flood_quota,
            latitude=street.latitude,
            longitude=street.longitude,
        )

    async def search_by_street(self, street_name: str) -> PlainAddress:
        address = await self.__address_repository.search_by_street(
            street_name=street_name
        )
        return address

    async def search_by_neighborhood(self, neighborhood_name: str) -> PlainAddress:
        address = await self.__address_repository.search_by_neighborhood(
            neighborhood_name=neighborhood_name
        )
        return address

    async def search_by_zip_code(self, zip_code: str) -> PlainAddress:
        address = await self.__address_repository.search_by_zip_code(zip_code=zip_code)
        return address

    async def search_all(self) -> List[PlainAddress]:
        address = await self.__address_repository.search_all()
        return address
