"""Generated model: CreateApprovalProcessTemplateRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field
from uuid import UUID
from typing import List, Optional, Union


class CreateApprovalProcessTemplateRequest(BaseConfigModel):
    name: str = Field(min_length=1, max_length=50)
    description: Optional[Union[str, Any]] = None
    steps: List[ApprovalTemplateStepRequest]
    move_to_folder_oid: Optional[Union[UUID, Any]] = None
