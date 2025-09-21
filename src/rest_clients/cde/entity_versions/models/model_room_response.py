"""Generated model: ModelRoomResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class ModelRoomResponse(BaseConfigModel):
    oid: UUID
    name: str
    number: str
    global_id: str
    checklist: bool
    items_count: str
    items_approved: str
    items_refused: str
    element_id: Optional[Union[str, Any]] = None
    ifc_id: Optional[Union[int, Any]] = None
    equipment_ifc_ids: List[int] = []
