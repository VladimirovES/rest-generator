"""Generated model: UpdatedCheckListItemsResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class UpdatedCheckListItemsResponseSchema(BaseConfigModel):
    checklist_oid: UUID
    assignment: UserShortResponseSchema
    category_name: Optional[Union[str, Any]] = None
    checklist_items: List[ShortCheckListItemResponse]
