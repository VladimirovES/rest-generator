"""Generated model: ModelSystemChecklistResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class ModelSystemChecklistResponse(BaseConfigModel):
    oid: UUID
    project_oid: UUID
    entity_oid: UUID
    entity_version_oid: UUID
    room_oid: Optional[Union[UUID, Any]] = None
    system_oid: UUID
    name: str = Field(max_length=300)
    type: CheckListType
    assignment: UserShortDTO
    creator: UserShortDTO
    created_at: datetime
    section: Optional[Union[str, Any]] = None
    floor: Optional[Union[str, Any]] = None
    categories_count: str
    categories: List[ChecklistCategoryResponse]
    contractor: Optional[Union[str, Any]] = None
    approval_status: Optional[Union[ApprovalProcessStatus, Any]] = None
