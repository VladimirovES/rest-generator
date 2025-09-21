"""Generated model: InspectorResult."""

from pydantic import BaseModel
from datetime import datetime
from typing import Any, List, Optional, Union
from . import InspectorStatus, ProbeResult


class InspectorResult(BaseModel):
    status: InspectorStatus
    timestamp: datetime = "2025-08-14T15:47:22.023202Z"
    duration: float
    dependencies: Optional[Union[List[ProbeResult], Any]] = None
