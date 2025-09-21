"""Generated model: RoleGroupResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Union


class RoleGroupResponse(BaseConfigModel):
    oid: UUID
    name: str
    permissions: List[Union[RolePermissionResponse, Any]]
    is_editable: bool
