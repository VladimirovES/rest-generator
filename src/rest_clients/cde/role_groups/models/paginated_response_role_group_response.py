"""Generated model: PaginatedResponse_RoleGroupResponse_."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union
from pydantic import AnyUrl


class PaginatedResponse_RoleGroupResponse_(BaseConfigModel):
    results: List[RoleGroupResponse]
    next: Optional[Union[AnyUrl, Any]] = None
    previous: Optional[Union[AnyUrl, Any]] = None
    count: int
