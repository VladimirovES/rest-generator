"""Generated model: CheckListCreateRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import Optional, Union


class CheckListCreateRequest(BaseConfigModel):
    entity_oid: UUID
    entity_version_oid: UUID
    room_oid: Optional[Union[UUID, Any]] = None
    system_oid: Optional[Union[UUID, Any]] = None
    name: Optional[Union[str, Any]] = None
    type: CheckListType
    assignment_oid: UUID
    contractor: Optional[Union[str, Any]] = None
    floor: Optional[Union[str, Any]] = None
    section: Optional[Union[str, Any]] = None
    global_id: Optional[Union[str, Any]] = None
