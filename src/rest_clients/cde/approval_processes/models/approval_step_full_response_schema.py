"""Generated model: ApprovalStepFullResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import date, datetime
from uuid import UUID
from typing import List, Optional, Union


class ApprovalStepFullResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    deadline: Optional[Union[date, Any]] = None
    minimal_approves_number: Optional[Union[int, Any]] = None
    status: ApprovalProcessStatus = "in_progress"
    approving_users: List[UserApproveResponseSchema]
    completed_at: Optional[Union[datetime, Any]] = None
    updated_at: Optional[Union[datetime, Any]] = None
