from app.core.db import DBConnection
from app.core.db.repositories.base_repository import Repository
from app.core.entities import StreetInDB, Street
from app.core.configs import get_logger

_logger = get_logger(__name__)


class StreetRepository(Repository):
    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    async def insert(self, street: Street) -> StreetInDB:
        try:
            query = """
             INSERT INTO public.streets(
                name, neighborhood_id, zip_code, flood_quota, latitude, longitude)
            VALUES(%(name)s, %(neighborhood_id)s, %(zip_code)s, %(flood_quota)s, %(latitude)s, %(longitude)s)
            RETURNING id, name, neighborhood_id, zip_code, flood_quota, latitude, longitude;
            """

            raw_street = await self.conn.execute(
                sql_statement=query, values=street.model_dump()
            )

            if raw_street:
                return StreetInDB(**raw_street)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {street.model_dump_json()}")

    async def select_by_id(self, id: int) -> StreetInDB:
        try:
            query = "SELECT id, name, neighborhood_id, zip_code, flood_quota, latitude, longitude FROM public.streets WHERE id=%(id)s;"

            raw_street = await self.conn.execute(sql_statement=query, values={"id": id})

            if raw_street:
                return StreetInDB(**raw_street)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")

    async def select_by_name(self, name: str) -> StreetInDB:
        try:
            query = "SELECT id, name, neighborhood_id, zip_code, flood_quota, latitude, longitude FROM public.streets WHERE name=%(name)s;"

            raw_street = await self.conn.execute(
                sql_statement=query, values={"name": name}
            )

            if raw_street:
                return StreetInDB(**raw_street)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")

    async def select_by_zip_code(self, zip_code: str) -> StreetInDB:
        try:
            query = "SELECT id, name, neighborhood_id, zip_code, flood_quota, latitude, longitude FROM public.streets WHERE zip_code=%(zip_code)s;"

            raw_street = await self.conn.execute(
                sql_statement=query, values={"zip_code": zip_code}
            )

            if raw_street:
                return StreetInDB(**raw_street)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(zip_code=zip_code)}")
