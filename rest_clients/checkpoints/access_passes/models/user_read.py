"""Generated model: UserRead."""

from pydantic import BaseModel
from uuid import UUID
from typing import Any, Union


class UserRead(BaseModel):
    oid: UUID
    first_name: str
    last_name: str
    middle_name: Union[str, Any]
