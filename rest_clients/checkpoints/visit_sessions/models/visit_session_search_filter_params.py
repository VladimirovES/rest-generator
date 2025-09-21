"""Generated model: VisitSessionSearchFilterParams."""

from pydantic import BaseModel
from datetime import date
from uuid import UUID
from typing import Any, List, Optional, Union


class VisitSessionSearchFilterParams(BaseModel):
    search: Optional[Union[str, Any]] = None
    start_date: Optional[Union[date, Any]] = None
    end_date: Optional[Union[date, Any]] = None
    checkpoint_oids: Optional[Union[List[UUID], Any]] = None
    users_oids: Optional[Union[List[UUID], Any]] = None
