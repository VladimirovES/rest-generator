"""Generated model: IssueResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import date, datetime
from uuid import UUID
from typing import Any, Dict, List, Optional, Union


class IssueResponseSchema(BaseConfigModel):
    oid: Optional[Union[UUID, Any]] = None
    project_oid: UUID
    title: str
    message: Optional[Union[str, Any]] = None
    deadline: date
    created_at: Optional[Union[datetime, Any]] = None
    fixed_version: Optional[Union[str, Any]] = None
    expired: bool
    position: PositionSchema
    additional_info: Union[Dict[str, Any], Any] = {}
    created_version: Optional[Union[str, Any]] = None
    entity: Optional[Union[EntityShortSchema, Any]] = None
    creator: UserShortSchema
    assignee: UserShortSchema
    status: IssueStatusBaseSchema
    files: List[FileBaseSchema] = []
    comments: List[IssueCommentBaseSchema] = []
    current: bool = False
    new_statuses: List[IssueStatusBaseSchema] = []
