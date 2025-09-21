"""Generated model: Files."""

from pydantic import BaseModel
from uuid import UUID


class Files(BaseModel):
    oid: UUID
    name: str
    url: str
    agreed_document: bool
