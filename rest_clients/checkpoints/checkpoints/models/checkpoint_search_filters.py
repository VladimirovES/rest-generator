"""Generated model: CheckpointSearchFilters."""

from pydantic import BaseModel
from typing import Any, Optional, Union


class CheckpointSearchFilters(BaseModel):
    search: Optional[Union[str, Any]] = None
