"""Generated model: PatchFolderRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import Any, Dict, List, Optional, Union


class PatchFolderRequest(BaseConfigModel):
    oid: Optional[Union[UUID, Any]] = None
    name: Optional[Union[str, Any]] = None
    parent_folder_oid: Optional[Union[UUID, Any]] = None
    additional_info: Dict[str, Any] = {}
    child_folders: Optional[Union[List[CreateFolderRequest], Any]] = None
