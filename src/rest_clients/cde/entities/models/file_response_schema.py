"""Generated model: FileResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import Optional, Union


class FileResponseSchema(BaseConfigModel):
    oid: UUID
    filename: str
    unique_filename: str
    mime_type: Optional[Union[str, Any]] = None
    url: Optional[Union[str, Any]] = None
