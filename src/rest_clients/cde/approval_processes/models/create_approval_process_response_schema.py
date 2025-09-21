"""Generated model: CreateApprovalProcessResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class CreateApprovalProcessResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    created_at: datetime
    status: str = "in_progress"
    description: Optional[Union[str, Any]] = None
    updated_at: datetime
    entities: List[EntityToApproveRequest]
    folder_oids: Optional[Union[List[UUID], Any]] = None
    steps: Optional[Union[List[CreateApprovalStepResponse], Any]] = None
    move_to_folder_oid: Optional[Union[UUID, Any]] = None
    template_oid: Optional[Union[UUID, Any]] = None
