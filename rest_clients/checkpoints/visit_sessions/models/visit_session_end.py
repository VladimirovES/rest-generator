"""Generated model: VisitSessionEnd."""

from pydantic import BaseModel
from datetime import datetime
from typing import Any, Union
from . import UserRead


class VisitSessionEnd(BaseModel):
    visit_end: Union[datetime, Any]
    closed_by: Union[UserRead, Any]
