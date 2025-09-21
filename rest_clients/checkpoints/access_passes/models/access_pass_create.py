"""Generated model: AccessPassCreate."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, List, Optional, Union
from . import GuestInfo, VehicleCreate


class AccessPassCreate(BaseModel):
    started_at: datetime
    ended_at: datetime
    guest: GuestInfo
    comment: Optional[Union[str, Any]] = None
    vehicle: Optional[Union[VehicleCreate, Any]] = None
    contact_info: Optional[Union[ContactInfo - Input, Any]] = None
    checkpoint_oid: UUID
    pass_type: Optional[Union[bool, Any]] = None
    files: Optional[List[UUID]] = None
