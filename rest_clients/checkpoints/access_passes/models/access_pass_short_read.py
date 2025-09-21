"""Generated model: AccessPassShortRead."""

from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Any, Union


class AccessPassShortRead(BaseModel):
    oid: UUID
    status: common__dto__StatusRead
    created_at: datetime
    updated_at: Union[datetime, Any]
