"""Generated model: ApprovalProcessChecklistResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class ApprovalProcessChecklistResponseSchema(BaseConfigModel):
    oid: UUID
    checklist_oid: UUID
    name: str
    description: Optional[Union[str, Any]] = None
    status: ApprovalProcessStatus
    entities: List[Entity]
    steps: List[CreateApprovalStepResponse]
    folder_storage_checklist_oid: Optional[Union[UUID, Any]] = None
    move_to_folder_oid: Optional[Union[UUID, Any]] = None
    template_oid: Optional[Union[UUID, Any]] = None
    created_at: datetime
    updated_at: datetime
