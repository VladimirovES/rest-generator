"""Generated model: FileResponse."""

from pydantic import BaseModel
from uuid import UUID


class FileResponse(BaseModel):
    oid: UUID
    name: str
