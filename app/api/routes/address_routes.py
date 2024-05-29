from fastapi import APIRouter, Depends, Path, Security
from fastapi.exceptions import HTTPException
from unidecode import unidecode
from app.api.composers import address_composer
from app.api.dependencies.authenticate import user_authentication
from app.core.entities.user import UserInDB
from app.core.services import AddressServices
from app.core.entities import Address

router = APIRouter(prefix="/address", tags=["Address"])


@router.post("")
async def create_address(
    address: Address,
    services: AddressServices = Depends(address_composer)
):
    address = await services.create(address=address)

    if not address:
        raise HTTPException(status_code=400, detail="Some error happen")

    return address

@router.get("")
async def get_address(
    services: AddressServices = Depends(address_composer),
    user_authentication: UserInDB = Security(user_authentication, scopes="")
):
    address = await services.search_all()

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address

@router.get("/zip-code/{zip_code}")
async def get_address_by_zip_code(
    zip_code: str = Path(pattern=r"^\d{5}-\d{3}$"),
    services: AddressServices = Depends(address_composer),
    user_authentication: UserInDB = Security(user_authentication, scopes="")
):
    address = await services.search_by_zip_code(zip_code=zip_code)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address

@router.get("/street/{street_name}")
async def get_address_by_street(
    street_name: str,
    services: AddressServices = Depends(address_composer),
    user_authentication: UserInDB = Security(user_authentication, scopes="")
):
    street_name = unidecode(street_name).title()
    address = await services.search_by_street(street_name=street_name)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address

@router.get("/neighborhood/{neighborhood_name}")
async def get_address_by_neighborhood(
    neighborhood_name: str,
    services: AddressServices = Depends(address_composer),
    user_authentication: UserInDB = Security(user_authentication, scopes="")
):
    neighborhood_name = unidecode(neighborhood_name).title()
    address = await services.search_by_neighborhood(neighborhood_name=neighborhood_name)

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    return address
