"""Generated model: PaginatedResponse_UserWithPermissionResponse_."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union
from pydantic import AnyUrl


class PaginatedResponse_UserWithPermissionResponse_(BaseConfigModel):
    results: List[UserWithPermissionResponse]
    next: Optional[Union[AnyUrl, Any]] = None
    previous: Optional[Union[AnyUrl, Any]] = None
    count: int
