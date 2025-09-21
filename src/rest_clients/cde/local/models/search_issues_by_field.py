"""Generated model: SearchIssuesByField."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class SearchIssuesByField(BaseConfigModel):
    field: Optional[Union[str, Any]] = None
    search: Optional[Union[str, Any]] = None
    user_oid: Optional[Union[UUID, Any]] = None
    project_oid: Optional[Union[UUID, Any]] = None
    user_roles: Optional[Union[List[str], Any]] = None
