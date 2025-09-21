"""Generated model: AuthorRead."""

from pydantic import BaseModel
from uuid import UUID
from typing import Any, Optional, Union


class AuthorRead(BaseModel):
    oid: UUID
    first_name: Optional[Union[str, Any]] = None
    last_name: Optional[Union[str, Any]] = None
    middle_name: Optional[Union[str, Any]] = None
    position: Optional[Union[str, Any]] = None
    company_name: Optional[Union[str, Any]] = None
    photo: Optional[Union[str, Any]] = None
