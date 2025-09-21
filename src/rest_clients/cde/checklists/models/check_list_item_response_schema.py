"""Generated model: CheckListItemResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from datetime import datetime
from uuid import UUID
from typing import Optional, Union


class CheckListItemResponseSchema(BaseConfigModel):
    checklist_oid: UUID
    oid: UUID
    name: str
    category: str
    mark: Optional[Union[str, Any]] = None
    units: Optional[Union[str, Any]] = None
    fact_units: Optional[Union[str, Any]] = None
    unit_type: Optional[Union[str, Any]] = None
    status: CheckListItemStatus
    comment: Optional[Union[str, Any]] = None
    updated_at: datetime
