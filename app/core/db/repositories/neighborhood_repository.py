from app.core.db import DBConnection
from app.core.db.repositories.base_repository import Repository
from app.core.entities import NeighborhoodInDB, Neighborhood
from app.core.configs import get_logger

_logger = get_logger(__name__)


class NeighborhoodRepository(Repository):
    def __init__(self, connection: DBConnection) -> None:
        super().__init__(connection)

    async def insert(self, neighborhood: Neighborhood) -> NeighborhoodInDB:
        try:
            query = """--sql
            INSERT INTO public.neighborhoods("name", population, houses, area)
            VALUES(%(name)s, %(population)s, %(houses)s, %(area)s)
            RETURNING id, name, population, houses, area;
            """

            raw_neighborhood = await self.conn.execute(
                sql_statement=query, values={
                    "name": neighborhood.name,
                    "population": neighborhood.population,
                    "houses": neighborhood.houses,
                    "area": neighborhood.area,
                }
            )

            if raw_neighborhood:
                return NeighborhoodInDB(**raw_neighborhood)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {neighborhood.model_dump_json()}")

    async def select_by_id(self, id: int) -> NeighborhoodInDB:
        try:
            query = 'SELECT id, "name", population, houses, area FROM public.neighborhoods WHERE id=%(id)s;'

            raw_neighborhood = await self.conn.execute(sql_statement=query, values={"id": id})

            if raw_neighborhood:
                return NeighborhoodInDB(**raw_neighborhood)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(id=id)}")

    async def select_by_name(self, name: str) -> NeighborhoodInDB:
        try:
            query = "SELECT id, name, population, houses, area FROM public.neighborhoods WHERE name ILIKE %(name)s ESCAPE '';"

            raw_neighborhood = await self.conn.execute(
                sql_statement=query, values={"name": "%{}%".format(name)}
            )

            if raw_neighborhood:
                return NeighborhoodInDB(**raw_neighborhood)

        except Exception as error:
            _logger.error(f"Error: {str(error)}. Data: {dict(name=name)}")
