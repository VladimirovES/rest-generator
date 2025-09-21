"""Generated model: CheckListRetrieveResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class CheckListRetrieveResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    entity_name: str
    version_number: str
    creator: UserShortResponseSchema
    assignment: UserShortResponseSchema
    type: CheckListType
    created_at: datetime
    updated_at: datetime
    list_name: Union[str, Any]
    floor: Union[str, Any]
    section: Union[str, Any]
    room_oid: Optional[Union[UUID, Any]] = None
    system_oid: Optional[Union[UUID, Any]] = None
    content: List[CheckListItemResponse] = []
    is_finished: bool
    approval_status: Optional[Union[ApprovalProcessStatus, Any]] = None
