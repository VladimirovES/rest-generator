"""Generated model: SearchApprovalProcessesLogsRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class SearchApprovalProcessesLogsRequest(BaseConfigModel):
    page: int = 1
    per_page: int = 10
    filters: Optional[Union[ApprovalProcessesLogsFilter, Any]] = None
