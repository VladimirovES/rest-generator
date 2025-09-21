"""Generated model: Vehicle."""

from pydantic import BaseModel
from uuid import UUID


class Vehicle(BaseModel):
    oid: UUID
    brand: str
    number: str
