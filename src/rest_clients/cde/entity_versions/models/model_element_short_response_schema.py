"""Generated model: ModelElementShortResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import Optional, Union


class ModelElementShortResponseSchema(BaseConfigModel):
    oid: UUID
    ifc_id: Optional[Union[int, Any]] = None
    element_id: Optional[Union[str, Any]] = None
