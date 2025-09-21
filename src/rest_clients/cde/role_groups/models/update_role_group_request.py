"""Generated model: UpdateRoleGroupRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field
from uuid import UUID
from typing import List


class UpdateRoleGroupRequest(BaseConfigModel):
    name: str = Field(min_length=1, max_length=50)
    permissions: List[UUID]
