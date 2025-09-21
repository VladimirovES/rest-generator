"""Generated model: CheckpointUpdate."""

from pydantic import BaseModel
from pydantic import Field


class CheckpointUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
