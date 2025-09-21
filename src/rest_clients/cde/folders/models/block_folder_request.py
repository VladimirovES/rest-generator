"""Generated model: BlockFolderRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID


class BlockFolderRequest(BaseConfigModel):
    oid: UUID
