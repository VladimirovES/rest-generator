"""Generated model: CheckpointSearchData."""

from pydantic import BaseModel
from pydantic import Field
from typing import Any, List, Optional, Union
from . import CheckpointSearchFilters


class CheckpointSearchData(BaseModel):
    page: int = Field(default=1, ge=1.0)
    page_size: int = Field(default=50, ge=1.0, le=500.0)
    filters: Optional[Union[CheckpointSearchFilters, Any]] = None
    sort: List[str] = ["-created_at"]
