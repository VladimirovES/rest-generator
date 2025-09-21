"""Generated model: ListIssueResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class ListIssueResponseSchema(BaseConfigModel):
    objects: List[IssueSchema]
