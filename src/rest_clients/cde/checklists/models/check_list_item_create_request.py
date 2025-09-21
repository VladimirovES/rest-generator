"""Generated model: CheckListItemCreateRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union


class CheckListItemCreateRequest(BaseConfigModel):
    category_name: Optional[Union[str, Any]] = None
    checklist_items: List[CheckListItemRequest]
    revit_tags: Optional[Union[List[str], Any]] = None
    ifc_ids: Optional[Union[List[int], Any]] = None
