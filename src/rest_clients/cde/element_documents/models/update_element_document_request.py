"""Generated model: UpdateElementDocumentRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field


class UpdateElementDocumentRequest(BaseConfigModel):
    name: str = Field(max_length=100)
    reference: str = Field(max_length=1000)
