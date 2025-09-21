"""Generated model: VisitSessionSearchResponse."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, Union
from . import UserRead, Vehicle


class VisitSessionSearchResponse(BaseModel):
    oid: UUID
    title: str
    visit_start: datetime
    visit_end: Union[datetime, Any]
    visitor: Union[UserRead, Any]
    vehicle: Union[Vehicle, Any]
