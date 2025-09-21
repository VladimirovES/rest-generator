"""Generated model: CheckBlockFolderResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID


class CheckBlockFolderResponse(BaseConfigModel):
    folder_oid: UUID
    is_block: bool
