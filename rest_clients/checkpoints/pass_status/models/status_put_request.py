"""Generated model: StatusPutRequest."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, Optional, Union
from . import StatusBase


class StatusPutRequest(BaseModel):
    pass_id: UUID
    status: StatusBase
    created_at: Optional[Union[datetime, Any]] = None
    updated_at: Optional[Union[datetime, Any]] = None
