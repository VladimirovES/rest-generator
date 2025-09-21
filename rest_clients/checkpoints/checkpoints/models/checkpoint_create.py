"""Generated model: CheckpointCreate."""

from pydantic import BaseModel
from pydantic import Field


class CheckpointCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
