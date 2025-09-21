"""Generated model: CreateIssueResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID


class CreateIssueResponseSchema(BaseConfigModel):
    oid: UUID
