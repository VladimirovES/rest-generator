"""Generated model: EntitiesFilters."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional, Union


class EntitiesFilters(BaseConfigModel):
    is_deleted: Optional[Union[bool, Any]] = None
    oid__in: Optional[Union[List[UUID], Any]] = None
    creator_oid__in: Optional[Union[List[UUID], Any]] = None
    type__in: Optional[Union[List[EntityType], Any]] = None
    folder_oid__in: Optional[Union[List[UUID], Any]] = None
    version__in: Optional[Union[List[int], Any]] = None
    status__in: Optional[Union[List[str], Any]] = None
