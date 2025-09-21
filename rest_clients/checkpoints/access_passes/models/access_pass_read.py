"""Generated model: AccessPassRead."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, List, Optional, Union
from . import CheckpointShortRead, FileRead, UserRead, VehicleCreate, VisitSessionBase


class AccessPassRead(BaseModel):
    oid: UUID
    status: common__dto__StatusRead
    created_at: datetime
    updated_at: Union[datetime, Any]
    title: str
    comment: Union[str, Any]
    started_at: datetime
    ended_at: datetime
    vehicle: Union[VehicleCreate, Any]
    visitor: UserRead
    contact_info: Union[api__handlers__access_pass__dto__ContactInfo, Any]
    author: UserRead
    pass_type: bool
    checkpoint: CheckpointShortRead
    visit_session: Optional[Union[VisitSessionBase, Any]] = None
    files: List[FileRead] = []
