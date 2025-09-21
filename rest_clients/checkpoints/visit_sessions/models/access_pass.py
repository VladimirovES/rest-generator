"""Generated model: AccessPass."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, List, Optional, Union
from . import Checkpoint, Files, Status, UserRead, Vehicle


class AccessPass(BaseModel):
    oid: UUID
    created_at: datetime
    updated_at: Union[datetime, Any]
    title: str
    status: Status
    started_at: Union[datetime, Any]
    ended_at: Union[datetime, Any]
    visitor: Optional[Union[UserRead, Any]] = None
    vehicle: Union[Vehicle, Any]
    contact_info: Union[api__handlers__visit_sessions__dto__ContactInfo, Any]
    comment: Union[str, Any]
    checkpoint: Union[Checkpoint, Any]
    files: Union[List[Files], Any]
    author: Union[UserRead, Any]
