"""Generated model: CreateApprovalProcessChecklistRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class CreateApprovalProcessChecklistRequest(BaseConfigModel):
    name: str
    description: Optional[Union[str, Any]] = None
    checklist_oid: UUID
    steps: List[ApprovalStepRequest]
    folder_storage_checklist_oid: UUID
    move_to_folder_oid: Optional[Union[UUID, Any]] = None
    template_oid: Optional[Union[UUID, Any]] = None
