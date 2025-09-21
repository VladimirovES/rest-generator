"""Generated model: EntityVersionListResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import Optional, Union


class EntityVersionListResponseSchema(BaseConfigModel):
    oid: UUID
    version_number: str
    created_at: datetime
    deleted_at: Optional[Union[datetime, Any]] = None
    comment: Optional[Union[str, Any]] = None
    size: Optional[Union[int, Any]] = None
    user: Optional[Union[UserShortSchema, Any]] = None
    entity_name: Optional[Union[str, Any]] = None
    type: Optional[Union[EntityType, Any]] = None
    approval_process: Optional[Union[ApprovalProcessResponseSchemaBase, Any]] = None
