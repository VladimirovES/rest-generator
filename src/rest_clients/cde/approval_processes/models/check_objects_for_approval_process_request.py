"""Generated model: CheckObjectsForApprovalProcessRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class CheckObjectsForApprovalProcessRequest(BaseConfigModel):
    entities: Optional[Union[List[EntityToApproveRequest], Any]] = None
    folder_oids: Optional[Union[List[UUID], Any]] = None
