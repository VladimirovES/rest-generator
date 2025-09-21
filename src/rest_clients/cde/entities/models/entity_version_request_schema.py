"""Generated model: EntityVersionRequestSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union


class EntityVersionRequestSchema(BaseConfigModel):
    files: List[FileRequestSchema]
    is_changes: bool = False
    comment: Optional[Union[str, Any]] = None
