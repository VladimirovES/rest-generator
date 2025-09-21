"""Generated model: AccessPassSearchFilters."""

from pydantic import BaseModel
from datetime import date
from uuid import UUID
from typing import Any, List, Optional, Union


class AccessPassSearchFilters(BaseModel):
    search: Optional[Union[str, Any]] = None
    started_at: Optional[Union[date, Any]] = None
    ended_at: Optional[Union[date, Any]] = None
    checkpoint_oids: Optional[Union[List[UUID], Any]] = None
    status_oids: Optional[Union[List[UUID], Any]] = None
    author_oids: Optional[Union[List[UUID], Any]] = None
