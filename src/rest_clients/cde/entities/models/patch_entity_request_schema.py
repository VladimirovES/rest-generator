"""Generated model: PatchEntityRequestSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Any, Dict, Optional, Union


class PatchEntityRequestSchema(BaseConfigModel):
    name: Optional[Union[str, Any]] = None
    preview: Optional[Union[FileRequestSchema, Any]] = None
    additional_info: Optional[Union[Dict[str, Any], Any]] = None
