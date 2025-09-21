"""Generated model: AccessPassPDFResponse."""

from pydantic import BaseModel
from uuid import UUID


class AccessPassPDFResponse(BaseModel):
    oid: UUID
    name: str
