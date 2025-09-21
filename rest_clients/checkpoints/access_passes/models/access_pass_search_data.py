"""Generated model: AccessPassSearchData."""

from pydantic import BaseModel
from pydantic import Field
from typing import Any, List, Optional, Union
from . import AccessPassSearchFilters


class AccessPassSearchData(BaseModel):
    page: int = Field(default=1, ge=1.0)
    page_size: int = Field(default=50, ge=1.0, le=500.0)
    filters: Optional[Union[AccessPassSearchFilters, Any]] = None
    sort: List[str] = ["-created_at"]
