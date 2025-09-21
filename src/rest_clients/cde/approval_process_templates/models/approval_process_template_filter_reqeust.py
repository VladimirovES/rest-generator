"""Generated model: ApprovalProcessTemplateFilterReqeust."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class ApprovalProcessTemplateFilterReqeust(BaseConfigModel):
    name: Optional[Union[str, Any]] = None
    author: Optional[Union[str, Any]] = None
    filters: Optional[
        Union[presentation__schemas__approval_processes__filters__Filters, Any]
    ] = None
    page: Union[int, Any] = 1
    per_page: Union[int, Any] = 10
