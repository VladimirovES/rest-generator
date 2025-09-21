"""Generated model: PaginatedApprovalProcessTemplateResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class PaginatedApprovalProcessTemplateResponse(BaseConfigModel):
    objects: List[ApprovalProcessTemplateResponseShortSchema]
    current_page: int
    total_pages: int
    page_size: int
    total_items: int
