"""Generated model: FileRead."""

from pydantic import BaseModel
from uuid import UUID


class FileRead(BaseModel):
    oid: UUID
    name: str
    url: str
    agreed_document: bool
