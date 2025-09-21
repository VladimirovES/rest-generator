"""Generated model: GuestInfo."""

from pydantic import BaseModel
from pydantic import Field
from typing import Any, Optional, Union


class GuestInfo(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    middle_name: Optional[Union[str, Any]] = None
