"""Generated model: MoveFolderRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID


class MoveFolderRequest(BaseConfigModel):
    parent_folder_oid: UUID
    save_roles: bool
