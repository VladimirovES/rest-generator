"""Generated model: PropertyModelSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class PropertyModelSchema(BaseConfigModel):
    room_oid: Optional[Union[UUID, Any]] = None
    system_oid: Optional[Union[UUID, Any]] = None
    element_oid: Optional[Union[UUID, Any]] = None
    param_groups: List[ParamGroupResponseSchema] = []
    revit_id: Union[str, Any]
    global_id: Union[str, Any]
    name: str
    room_number: Union[str, Any]
