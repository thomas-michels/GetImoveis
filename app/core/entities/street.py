from typing import Optional
from pydantic import BaseModel, Field
from app.core.utils import MyStr


class Street(BaseModel):
    name: MyStr = Field(example="Antonio da Veiga")
    neighborhood_id: int = Field(example=123)
    zip_code: Optional[MyStr] = Field(default=None, example="89012-500", pattern=r'^\d{5}-\d{3}$')
    latitude: Optional[MyStr] = Field(default=None, example="-26.8852955")
    longitude: Optional[MyStr] = Field(default=None, example="-49.0808952")
    flood_quota: Optional[float] = Field(default=None, example=10.5)


class StreetInDB(Street):
    id: int = Field(example=123)
