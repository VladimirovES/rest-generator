"""Generated model: EntityVersionFullResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Union


class EntityVersionFullResponseSchema(BaseConfigModel):
    oid: UUID
    version_number: str = "1.0"
    created_at: datetime
    deleted_at: Optional[Union[datetime, Any]] = None
    comment: Optional[Union[str, Any]] = None
    size: Optional[Union[int, Any]] = None
    entity_name: Optional[Union[str, Any]] = None
    type: Optional[Union[EntityType, Any]] = None
    files: List[FileResponseSchema]
    approval_process: Optional[Union[ApprovalProcessResponseSchemaBase, Any]] = None
    creator: Optional[Union[UserShortSchema, Any]] = None
