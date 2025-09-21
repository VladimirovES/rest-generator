"""Generated model: ApprovalProcessTemplateFullResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class ApprovalProcessTemplateFullResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    description: Optional[Union[str, Any]] = None
    steps: List[ApprovalProcessTemplateStepResponseSchema]
    move_to_folder: Optional[Union[FolderPathResponse, Any]] = None
    created_at: datetime
    updated_at: datetime
