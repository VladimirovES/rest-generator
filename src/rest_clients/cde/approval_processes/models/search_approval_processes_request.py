"""Generated model: SearchApprovalProcessesRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class SearchApprovalProcessesRequest(BaseConfigModel):
    page: int = 1
    per_page: int = 10
    scope: ApprovalProcessesScope
    filters: Optional[Union[ApprovalProcessesFilter, Any]] = None
