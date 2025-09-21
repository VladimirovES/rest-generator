"""Generated model: ProjectCreate."""

from pydantic import BaseModel
from uuid import UUID


class ProjectCreate(BaseModel):
    name: str
    oid: UUID
