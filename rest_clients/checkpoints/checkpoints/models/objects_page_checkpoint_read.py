"""Generated model: ObjectsPage_CheckpointRead_."""

from pydantic import BaseModel
from typing import Any, List, Union
from . import CheckpointRead


class ObjectsPage_CheckpointRead_(BaseModel):
    objects: List[CheckpointRead]
    current_page: Union[int, Any]
    total_pages: Union[int, Any]
    page_size: Union[int, Any]
    total_items: Union[int, Any]
