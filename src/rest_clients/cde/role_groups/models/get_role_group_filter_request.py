"""Generated model: GetRoleGroupFilterRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class GetRoleGroupFilterRequest(BaseConfigModel):
    role_group__in: Optional[Union[List[UUID], Any]] = None
    permission__in: Optional[Union[List[UUID], Any]] = None
    folder_oids: Optional[Union[List[UUID], Any]] = None
    entity_oids: Optional[Union[List[UUID], Any]] = None
    is_editable: Optional[Union[bool, Any]] = None
    search: Optional[Union[str, Any]] = None
    sort: Optional[Union[List[str], Any]] = None
