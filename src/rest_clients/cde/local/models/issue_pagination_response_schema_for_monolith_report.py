"""Generated model: IssuePaginationResponseSchemaForMonolithReport."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class IssuePaginationResponseSchemaForMonolithReport(BaseConfigModel):
    results: List[IssueReportSchema]
    meta: MetaIssuePaginationSchema
