"""Generated model: ChangeStatusIssueRequestSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class ChangeStatusIssueRequestSchema(BaseConfigModel):
    new_status: IssueStatusType
    fixed_version: Optional[Union[str, Any]] = None
