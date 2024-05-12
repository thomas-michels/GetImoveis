from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from app.api.composers import neighborhood_composer
from app.core.services import NeighborhoodServices
from app.core.entities import Neighborhood

router = APIRouter(prefix="/neighborhoods", tags=["Neighborhoods"])


@router.post("")
async def create_neighborhood(
    neighborhood: Neighborhood,
    services: NeighborhoodServices = Depends(neighborhood_composer),
):
    neighborhood_in_db = await services.create(neighborhood=neighborhood)

    if not neighborhood_in_db:
        raise HTTPException(status_code=400, detail="Some error happen")

    return neighborhood_in_db
