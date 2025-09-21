"""Generated model: PaginatedResponse_UserWithRoleGroupResponse_."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union
from pydantic import AnyUrl


class PaginatedResponse_UserWithRoleGroupResponse_(BaseConfigModel):
    results: List[UserWithRoleGroupResponse]
    next: Optional[Union[AnyUrl, Any]] = None
    previous: Optional[Union[AnyUrl, Any]] = None
    count: int
