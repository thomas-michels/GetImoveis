from typing import List
from app.core.db import DBConnection
from app.core.db.repositories.base_repository import Repository
from app.core.entities import PlainAddress
from app.core.configs import get_logger

_logger = get_logger(__name__)


class AddressRepository(Repository):
    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    async def search_all(self) -> List[PlainAddress]:
        try:
            results = await self.__select_address(many=True)

            address = []

            for result in results:
                address.append(PlainAddress(**result))

            return address

        except Exception as error:
            _logger.error(f"Error: {str(error)}")
            return []

    async def search_by_zip_code(self, zip_code: str) -> PlainAddress:
        try:
            query = " WHERE zip_code = %(zip_code)s;"
            result = await self.__select_address(
                where=query, values={"zip_code": zip_code}, many=False
            )

            if result:
                plain_address = PlainAddress(**result)
                return plain_address

        except Exception as error:
            _logger.error(f"Error: {str(error)}")

    async def search_by_street(self, street_name: str) -> PlainAddress:
        try:
            query = " WHERE s.name ILIKE %(street_name)s ESCAPE '';"
            result = await self.__select_address(
                where=query,
                many=False,
                values={"street_name": "%{}%".format(street_name)},
            )

            if result:
                plain_address = PlainAddress(**result)
                return plain_address

        except Exception as error:
            _logger.error(f"Error: {str(error)}")

    async def search_by_neighborhood(self, neighborhood_name: str) -> PlainAddress:
        try:
            query = f"""
            SELECT 
                n.id AS neighborhood_id,
                n."name" AS neighborhood_name,
                NULL AS street_id,
                NULL AS street_name,
                NULL AS zip_code,
                NULL AS flood_quota,
                NULL AS latitude,
                NULL AS longitude
            FROM public.neighborhoods n
            WHERE n.name ILIKE %(neighborhood_name)s ESCAPE '';
            """

            result = await self.conn.execute(
                sql_statement=query,
                values={"neighborhood_name": "%{}%".format(neighborhood_name)},
                many=False,
            )

            if result:
                plain_address = PlainAddress(**result)
                return plain_address

        except Exception as error:
            _logger.error(f"Error: {str(error)}")

    async def __select_address(
        self, where: str = None, values: dict = {}, many: bool = False
    ) -> List[dict]:
        query = f"""
            SELECT
                n.id AS neighborhood_id,
                n."name" AS neighborhood_name,
                s.id AS street_id,
                s."name" AS street_name,
                s.zip_code,
                s.flood_quota,
                s.latitude,
                s.longitude
            FROM
                public.streets s
            LEFT JOIN public.neighborhoods n ON
                s.neighborhood_id = n.id

            """

        if where:
            query += where

        results = await self.conn.execute(sql_statement=query, values=values, many=many)
        return results
