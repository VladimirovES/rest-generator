"""Generated model: IssueCommentResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import Union


class IssueCommentResponseSchema(BaseConfigModel):
    oid: Union[UUID, Any]
    created_at: datetime
    creator: UserBaseDTO
    comment: str
    project_oid: Union[UUID, Any]
    issue_oid: Union[UUID, Any]
