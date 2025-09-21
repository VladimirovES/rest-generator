"""Generated model: PagePaginatorResponse_ApprovalProcessLogResponseSchema_."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class PagePaginatorResponse_ApprovalProcessLogResponseSchema_(BaseConfigModel):
    objects: List[ApprovalProcessLogResponseSchema]
    current_page: int
    total_pages: int
    page_size: int
    total_items: int
