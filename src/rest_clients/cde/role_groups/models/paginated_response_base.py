"""Generated model: PaginatedResponseBase."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union
from pydantic import AnyUrl


class PaginatedResponseBase(BaseConfigModel):
    results: List[Any]
    next: Optional[Union[AnyUrl, Any]] = None
    previous: Optional[Union[AnyUrl, Any]] = None
    count: int
