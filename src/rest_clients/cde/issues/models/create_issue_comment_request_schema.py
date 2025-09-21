"""Generated model: CreateIssueCommentRequestSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field


class CreateIssueCommentRequestSchema(BaseConfigModel):
    comment: str = Field(max_length=500)
