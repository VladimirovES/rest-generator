"""Generated model: CountApprovalProcessesRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel


class CountApprovalProcessesRequest(BaseConfigModel):
    scope: ApprovalProcessesScope
    filters: StatusApprovalProcessFilter
