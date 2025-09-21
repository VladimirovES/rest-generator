"""Generated model: VehicleCreate."""

from pydantic import BaseModel
from pydantic import Field


class VehicleCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=50)
    number: str = Field(min_length=1, max_length=50)
