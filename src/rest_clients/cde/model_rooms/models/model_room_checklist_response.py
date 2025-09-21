"""Generated model: ModelRoomChecklistResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class ModelRoomChecklistResponse(BaseConfigModel):
    oid: UUID
    project_oid: UUID
    entity_oid: UUID
    entity_version_oid: UUID
    room_oid: UUID
    system_oid: Optional[Union[UUID, Any]] = None
    name: str = Field(max_length=300)
    type: CheckListType
    assignment: UserShortDTO
    creator: UserShortDTO
    created_at: datetime
    categories_count: str
    categories: List[ChecklistCategoryResponse]
    contractor: Optional[Union[str, Any]] = None
    approval_status: Optional[Union[ApprovalProcessStatus, Any]] = None
