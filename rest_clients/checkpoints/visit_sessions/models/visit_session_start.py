"""Generated model: VisitSessionStart."""

from pydantic import BaseModel
from datetime import datetime
from typing import Any, Union
from . import UserRead


class VisitSessionStart(BaseModel):
    visit_start: datetime
    opened_by: Union[UserRead, Any]
