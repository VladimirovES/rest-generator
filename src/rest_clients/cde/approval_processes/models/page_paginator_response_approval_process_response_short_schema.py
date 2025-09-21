"""Generated model: PagePaginatorResponse_ApprovalProcessResponseShortSchema_."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class PagePaginatorResponse_ApprovalProcessResponseShortSchema_(BaseConfigModel):
    objects: List[ApprovalProcessResponseShortSchema]
    current_page: int
    total_pages: int
    page_size: int
    total_items: int
