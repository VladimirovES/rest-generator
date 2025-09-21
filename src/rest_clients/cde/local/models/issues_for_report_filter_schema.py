"""Generated model: IssuesForReportFilterSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class IssuesForReportFilterSchema(BaseConfigModel):
    user_oid: Optional[Union[UUID, Any]] = None
    project_oid: Optional[Union[UUID, Any]] = None
    user_roles: Optional[Union[List[str], Any]] = None
    issue_title: Optional[Union[List[str], Any]] = None
    filename: Optional[Union[List[str], Any]] = None
    status: Optional[Union[List[str], Any]] = None
    created_at: Optional[Union[List[Union[str, datetime]], Any]] = None
    deadline: Optional[Union[List[Union[str, datetime]], Any]] = None
    creator: Optional[Union[List[str], Any]] = None
    assignee: Optional[Union[List[str], Any]] = None
    field_created_version: Optional[Union[List[str], Any]] = None
    field_fixed_version: Optional[Union[List[str], Any]] = None
    page: Union[int, Any] = 1
    per_page: Union[int, Any] = 10
