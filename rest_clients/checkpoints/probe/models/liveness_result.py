"""Generated model: LivenessResult."""

from pydantic import BaseModel
from datetime import datetime
from . import InspectorStatus


class LivenessResult(BaseModel):
    status: InspectorStatus
    timestamp: datetime = "2025-08-14T15:47:22.023202Z"
