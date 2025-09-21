"""Generated model: CheckListItemUpdateRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class CheckListItemUpdateRequest(BaseConfigModel):
    fact_units: str
    comment: Optional[Union[str, Any]] = None
    status: Optional[Union[CheckListItemStatus, Any]] = None
