"""Generated model: SetUsersForRoleGroupRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List


class SetUsersForRoleGroupRequest(BaseConfigModel):
    users: List[UUID]
