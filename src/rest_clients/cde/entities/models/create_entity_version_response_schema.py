"""Generated model: CreateEntityVersionResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import List


class CreateEntityVersionResponseSchema(BaseConfigModel):
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
