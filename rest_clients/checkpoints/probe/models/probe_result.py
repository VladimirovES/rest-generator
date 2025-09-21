"""Generated model: ProbeResult."""

from pydantic import BaseModel
from typing import Any, Optional, Union
from . import ProbeStatus


class ProbeResult(BaseModel):
    name: str
    info: Optional[Union[str, Any]] = None
    status: ProbeStatus
    duration: float
    error: Optional[Union[str, Any]] = None
