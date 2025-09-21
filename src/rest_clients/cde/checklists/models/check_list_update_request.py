"""Generated model: CheckListUpdateRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import Optional, Union


class CheckListUpdateRequest(BaseConfigModel):
    assignment_oid: UUID
    contractor: Optional[Union[ContractorResponse, Any]] = None
    floor: Optional[Union[str, Any]] = None
    section: Optional[Union[str, Any]] = None
    name: Optional[Union[str, Any]] = None
    is_finished: Optional[Union[bool, Any]] = None
