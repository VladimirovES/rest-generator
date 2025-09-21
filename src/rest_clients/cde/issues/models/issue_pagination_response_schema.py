"""Generated model: IssuePaginationResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union


class IssuePaginationResponseSchema(BaseConfigModel):
    objects: List[IssueSchema]
    current_page: Optional[Union[int, Any]] = None
    page_size: Optional[Union[int, Any]] = None
    total_items: Optional[Union[int, Any]] = None
    total_pages: int
