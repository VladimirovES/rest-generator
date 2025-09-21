"""Generated model: AuthorSearchData."""

from pydantic import BaseModel
from pydantic import Field
from typing import Any, List, Optional, Union
from . import AuthorSearchFilters


class AuthorSearchData(BaseModel):
    page: int = Field(default=1, ge=1.0)
    page_size: int = Field(default=50, ge=1.0, le=500.0)
    filters: Optional[Union[AuthorSearchFilters, Any]] = None
    sort: List[str] = ["first_name"]
