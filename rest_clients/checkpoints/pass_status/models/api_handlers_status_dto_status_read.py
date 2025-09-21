"""Generated model: api__handlers__status__dto__StatusRead."""

from pydantic import BaseModel
from uuid import UUID


class api__handlers__status__dto__StatusRead(BaseModel):
    name: str
    alias_name: str
    oid: UUID
    position: int
