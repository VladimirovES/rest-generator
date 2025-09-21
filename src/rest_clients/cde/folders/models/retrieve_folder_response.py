"""Generated model: RetrieveFolderResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import Any, Dict, Optional, Union


class RetrieveFolderResponse(BaseConfigModel):
    oid: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[Union[datetime, Any]] = None
    creator: UserResponseSchema
    project_oid: UUID
    parent_folder_oid: Optional[Union[UUID, Any]] = None
    additional_info: Union[Dict[str, Any], Any] = {}
    content: ContentFolderResponse
