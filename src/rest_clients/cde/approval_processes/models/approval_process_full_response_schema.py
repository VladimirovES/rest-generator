"""Generated model: ApprovalProcessFullResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class ApprovalProcessFullResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    created_at: datetime
    status: str = "in_progress"
    description: Optional[Union[str, Any]] = None
    updated_at: datetime
    creator: UserResponseSchema
    template: Optional[Union[ApprovalProcessTemplateResponseSchemaBase, Any]] = None
    move_to_folder: Optional[Union[FolderPathResponse, Any]] = None
    approval_objects: ContentFolderResponse
    steps: List[ApprovalStepResponseSchemaBase]
    current_step: Optional[Union[ApprovalStepFullResponseSchema, Any]] = None
    deleted_at: Optional[Union[datetime, Any]] = None
    remover: Optional[Union[UserResponseSchema, Any]] = None
