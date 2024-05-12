from pydantic import BaseModel, Field
from typing import Optional
from app.core.utils import MyStr


class Address(BaseModel):
    street: Optional[MyStr] = Field(
        example="Rua Antonio da Veiga",
    )
    neighborhood: Optional[MyStr] = Field(example="Viktor Konder")
    zip_code: Optional[MyStr] = Field(example="89012-500", pattern=r"^\d{5}-\d{3}$")
    latitude: Optional[MyStr] = Field(example="-26.8852955")
    longitude: Optional[MyStr] = Field(example="-49.0808952")
    flood_quota: Optional[float] = Field(example=10.5)


class PlainAddress(BaseModel):
    street_name: Optional[MyStr] = Field(
        example="Rua Antonio da Veiga",
    )
    street_id: Optional[int] = Field(example=123)
    neighborhood_name: Optional[MyStr] = Field(example="Viktor Konder")
    neighborhood_id: Optional[int] = Field(example=123)
    zip_code: Optional[MyStr] = Field(example="89012-500", pattern=r"^\d{5}-\d{3}$")
    latitude: Optional[MyStr] = Field(example="-26.8852955")
    longitude: Optional[MyStr] = Field(example="-49.0808952")
    flood_quota: Optional[float] = Field(example=10.5)
