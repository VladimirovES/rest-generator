"""Generated model: EntityFullResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import Any, Dict, List, Optional, Union


class EntityFullResponseSchema(BaseConfigModel):
    oid: UUID
    created_at: datetime
    updated_at: datetime
    name: str
    type: EntityType
    creator: UserResponseSchema
    current_version: EntityVersionResponseSchema
    project_oid: UUID
    folder_oid: UUID
    parent_folder_oids: List[UUID]
    additional_info: Dict[str, Any] = {}
    preview: Optional[Union[FileResponseSchema, Any]] = None
    deleted_at: Optional[Union[datetime, Any]] = None
    parent_folders: List[Any]
