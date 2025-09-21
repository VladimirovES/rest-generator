"""Generated model: SearchBodyFilters."""

from pydantic import BaseModel
from pydantic import Field
from typing import Any, List, Optional, Union
from . import VisitSessionSearchFilterParams


class SearchBodyFilters(BaseModel):
    page: int = Field(default=1, ge=1.0)
    page_size: int = Field(default=50, ge=1.0, le=500.0)
    filters: Optional[Union[VisitSessionSearchFilterParams, Any]] = None
    sort: Union[List[Sortitemenum], Any] = ["-visit_start"]
