"""Generated model: CheckListResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class CheckListResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    type: CheckListType
    created_at: datetime
    updated_at: Union[datetime, Any]
    entity_oid: UUID
    project_oid: UUID
    entity_version_oid: UUID
    deleted_at: Union[datetime, Any]
    floor: Union[str, Any]
    section: Union[str, Any]
    creator: UserShortResponseSchema
    assignment: UserShortResponseSchema
    categories_count: Optional[Union[int, Any]] = None
    categories: List[CategoryResponseSchema]
    global_oid: Optional[Union[str, Any]] = None
    approval_status: Optional[Union[ApprovalProcessStatus, Any]] = None
    contractor: Optional[Union[str, Any]] = None
    room_oid: Optional[Union[UUID, Any]] = None
    system_oid: Optional[Union[UUID, Any]] = None
    is_finished: bool
