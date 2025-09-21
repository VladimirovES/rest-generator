"""Generated model: AccessPassSearch."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, Union
from . import UserRead, VehicleCreate


class AccessPassSearch(BaseModel):
    oid: UUID
    status: common__dto__StatusRead
    created_at: datetime
    updated_at: Union[datetime, Any]
    started_at: datetime
    ended_at: datetime
    title: str
    vehicle: Union[VehicleCreate, Any]
    visitor: UserRead
