"""Generated model: ListIssueResponseSchemaForMonolithReport."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class ListIssueResponseSchemaForMonolithReport(BaseConfigModel):
    objects: List[IssueReportSchema]
