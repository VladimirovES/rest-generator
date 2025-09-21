"""Generated model: AuthorSearchFilters."""

from pydantic import BaseModel
from typing import Any, Optional, Union


class AuthorSearchFilters(BaseModel):
    author: Optional[Union[str, Any]] = None
