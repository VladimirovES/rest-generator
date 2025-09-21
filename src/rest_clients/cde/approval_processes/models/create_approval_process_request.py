"""Generated model: CreateApprovalProcessRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class CreateApprovalProcessRequest(BaseConfigModel):
    name: str
    description: Optional[Union[str, Any]] = None
    entities: Optional[Union[List[EntityToApproveRequest], Any]] = None
    folder_oids: Optional[Union[List[UUID], Any]] = None
    steps: Optional[Union[List[ApprovalStepRequest], Any]] = None
    move_to_folder_oid: Optional[Union[UUID, Any]] = None
    template_oid: Optional[Union[UUID, Any]] = None
    save_roles: Union[bool, Any] = False
