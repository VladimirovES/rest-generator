"""Generated model: CreatedCheckListItemsResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List


class CreatedCheckListItemsResponseSchema(BaseConfigModel):
    checklist_oid: UUID
    category_name: str
    checklist_items: List[ShortCheckListItemResponse]
