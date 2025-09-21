"""Generated model: CheckListRetrieveRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class CheckListRetrieveRequest(BaseConfigModel):
    category: Optional[Union[str, Any]] = None
