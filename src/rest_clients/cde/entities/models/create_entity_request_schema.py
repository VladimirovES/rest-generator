"""Generated model: CreateEntityRequestSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import Any, Dict, List, Optional, Union


class CreateEntityRequestSchema(BaseConfigModel):
    name: str
    type: EntityType
    folder_oid: UUID
    preview: Optional[Union[FileRequestSchema, Any]] = None
    files: List[FileRequestSchema]
    additional_info: Dict[str, Any] = {}
