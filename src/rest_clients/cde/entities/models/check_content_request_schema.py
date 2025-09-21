"""Generated model: CheckContentRequestSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class CheckContentRequestSchema(BaseConfigModel):
    name: str
    type: EntityType
    version_number: str
    files: List[CheckFileSchema]
