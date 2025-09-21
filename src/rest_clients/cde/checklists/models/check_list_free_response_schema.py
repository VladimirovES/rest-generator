"""Generated model: CheckListFreeResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class CheckListFreeResponseSchema(BaseConfigModel):
    oid: UUID
    project_oid: UUID
    entity_oid: UUID
    entity_version_oid: UUID
    room_oid: Union[UUID, str]
    system_oid: Union[UUID, str]
    name: str
    type: CheckListType
    assignment: UserShortResponseSchema
    creator: UserShortResponseSchema
    created_at: datetime
    categories_count: int
    categories: List[CategoryGroupedSchema]
    approval_status: Optional[Union[ApprovalProcessStatus, Any]] = None
    is_finished: bool
    contractor: Optional[Union[str, Any]] = None
