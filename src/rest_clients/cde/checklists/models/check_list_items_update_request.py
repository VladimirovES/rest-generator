"""Generated model: CheckListItemsUpdateRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class CheckListItemsUpdateRequest(BaseConfigModel):
    category_name: str
    created: Optional[Union[List[CheckListItemRequest], Any]] = None
    updated: Optional[Union[List[CheckListItemUUIDRequest], Any]] = None
    deleted_oids: Optional[Union[List[UUID], Any]] = None
