"""Generated model: VisitSessionBase."""

from pydantic import BaseModel
from uuid import UUID
from typing import Any, Optional, Union
from . import VisitSessionEnd, VisitSessionStart


class VisitSessionBase(BaseModel):
    oid: UUID
    start: VisitSessionStart
    end: Optional[Union[VisitSessionEnd, Any]] = None
