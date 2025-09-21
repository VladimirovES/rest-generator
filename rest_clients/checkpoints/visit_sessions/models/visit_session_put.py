"""Generated model: VisitSessionPut."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, Union
from . import UserRead


class VisitSessionPut(BaseModel):
    oid: UUID
    visit_start: datetime
    visit_end: datetime
    opened_by: Union[UserRead, Any]
    closed_by: Union[UserRead, Any]
