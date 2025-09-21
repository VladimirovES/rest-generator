"""Generated model: GetUsersFilterRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union


class GetUsersFilterRequest(BaseConfigModel):
    filters: Optional[Union[UsersFilterRequest, Any]] = None
    have_role_group: Optional[Union[bool, Any]] = None
    without_me: Optional[Union[bool, Any]] = None
    sort: Optional[Union[List[str], Any]] = None
