"""Generated model: ModelSystemChecklistRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID


class ModelSystemChecklistRequest(BaseConfigModel):
    entity_oid: UUID
    entity_version_oid: UUID
    global_id: str
