"""Generated model: CheckpointShortRead."""

from pydantic import BaseModel
from uuid import UUID


class CheckpointShortRead(BaseModel):
    oid: UUID
    name: str
