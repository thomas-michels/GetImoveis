from pydantic import BaseModel, Field
from typing import Optional
from app.core.utils import MyStr

class Neighborhood(BaseModel):
    name: MyStr = Field(example="Viktor Konder")
    population: Optional[int] = Field(default=None, example=123)
    houses: Optional[int] = Field(default=None, example=123)
    area: Optional[float] = Field(default=None, example=123)



class NeighborhoodInDB(Neighborhood):
    id: int = Field(example=123)
