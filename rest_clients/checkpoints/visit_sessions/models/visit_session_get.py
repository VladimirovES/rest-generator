"""Generated model: VisitSessionGet."""

from pydantic import BaseModel
from uuid import UUID
from typing import Any, Optional, Union
from . import AccessPass, VisitSessionEnd, VisitSessionStart


class VisitSessionGet(BaseModel):
    oid: UUID
    start: VisitSessionStart
    end: Optional[Union[VisitSessionEnd, Any]] = None
    access_pass: AccessPass
