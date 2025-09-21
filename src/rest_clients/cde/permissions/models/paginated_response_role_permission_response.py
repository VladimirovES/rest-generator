"""Generated model: PaginatedResponse_RolePermissionResponse_."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union
from pydantic import AnyUrl


class PaginatedResponse_RolePermissionResponse_(BaseConfigModel):
    results: List[RolePermissionResponse]
    next: Optional[Union[AnyUrl, Any]] = None
    previous: Optional[Union[AnyUrl, Any]] = None
    count: int
