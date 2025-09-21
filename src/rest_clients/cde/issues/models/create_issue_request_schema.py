"""Generated model: CreateIssueRequestSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field
from datetime import date
from uuid import UUID
from typing import List, Optional, Union


class CreateIssueRequestSchema(BaseConfigModel):
    assignee_oid: UUID
    title: str = Field(min_length=1, max_length=150)
    message: Optional[Union[str, Any]] = None
    deadline: date
    position: PositionSchema
    additional_info: Optional[Union[AdditionalInfoSchema, Any]] = None
    files: List[IssueFileRequestSchema]
