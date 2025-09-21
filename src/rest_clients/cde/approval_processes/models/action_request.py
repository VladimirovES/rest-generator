"""Generated model: ActionRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class ActionRequest(BaseConfigModel):
    action: ApproveAction
    comment: Optional[Union[str, Any]] = None
