"""Generated model: VisitSessionRead."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, Union
from . import UserRead


class VisitSessionRead(BaseModel):
    oid: UUID
    visit_start: datetime
    opened_by: Union[UserRead, Any]
