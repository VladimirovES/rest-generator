"""Generated model: Checkpoint."""

from pydantic import BaseModel
from uuid import UUID


class Checkpoint(BaseModel):
    oid: UUID
    name: str
