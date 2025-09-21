"""Generated model: CreateApprovalProcessTemplateResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class CreateApprovalProcessTemplateResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    description: Optional[Union[str, Any]] = None
    updated_at: datetime
    created_at: datetime
    steps: List[ApprovalProcessTemplateStepResponseSchema]
    move_to_folder_oid: Optional[Union[UUID, Any]] = None
