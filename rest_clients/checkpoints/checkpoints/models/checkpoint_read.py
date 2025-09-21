"""Generated model: CheckpointRead."""

from pydantic import BaseModel
from pydantic import Field
from datetime import datetime
from uuid import UUID
from typing import Any, Union


class CheckpointRead(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    oid: UUID
    created_at: datetime
    updated_at: Union[datetime, Any]
