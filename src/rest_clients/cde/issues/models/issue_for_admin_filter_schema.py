"""Generated model: IssueForAdminFilterSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class IssueForAdminFilterSchema(BaseConfigModel):
    oid: Optional[Union[UUID, Any]] = None
    oids: Optional[Union[List[UUID], Any]] = None
    project_oids: List[UUID]
    entity_oids: Optional[Union[List[UUID], Any]] = None
    creator_oids: Optional[Union[List[UUID], Any]] = None
    assignee_oids: Optional[Union[List[UUID], Any]] = None
    statuses: Optional[Union[List[str], Any]] = None
    entity_types: Optional[Union[List[EntityType], Any]] = None
    issue_title: Optional[Union[str, Any]] = None
    entity_name: Optional[Union[str, Any]] = None
    fixed_version: Optional[Union[str, Any]] = None
    creation_date_period: Optional[Union[DatetimePeriodSchema, Any]] = None
    deadline_period: Optional[Union[DatetimePeriodSchema, Any]] = None
    sort: Optional[Union[List[IssueSortSchema], Any]] = None
    page: Union[int, Any] = 1
    page_size: Union[int, Any] = 10
