"""Generated model: MoveEntityRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID


class MoveEntityRequest(BaseConfigModel):
    folder_oid: UUID
    save_roles: bool
