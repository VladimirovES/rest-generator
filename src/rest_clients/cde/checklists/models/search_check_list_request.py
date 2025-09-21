"""Generated model: SearchCheckListRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class SearchCheckListRequest(BaseConfigModel):
    filters: Optional[
        Union[presentation__schemas__checklists__filters__Filters, Any]
    ] = None
    page: Union[int, Any] = 1
    page_size: Union[int, Any] = 10
