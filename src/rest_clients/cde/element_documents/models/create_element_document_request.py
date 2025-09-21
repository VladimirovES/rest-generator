"""Generated model: CreateElementDocumentRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field


class CreateElementDocumentRequest(BaseConfigModel):
    name: str = Field(max_length=100)
    reference: str = Field(max_length=1000)
