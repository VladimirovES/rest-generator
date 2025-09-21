"""Generated model: AccessSettingResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class AccessSettingResponse(BaseConfigModel):
    users: List[UserWithPermissionAndRoleGroupResponse]
    role_groups: List[RoleGroupShortResponse]
