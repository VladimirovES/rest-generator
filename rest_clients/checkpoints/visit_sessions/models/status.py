"""Generated model: Status."""

from pydantic import BaseModel
from uuid import UUID


class Status(BaseModel):
    oid: UUID
    name: str
    alias_name: str
