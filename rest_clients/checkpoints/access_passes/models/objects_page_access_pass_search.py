"""Generated model: ObjectsPage_AccessPassSearch_."""

from pydantic import BaseModel
from typing import Any, List, Union
from . import AccessPassSearch


class ObjectsPage_AccessPassSearch_(BaseModel):
    objects: List[AccessPassSearch]
    current_page: Union[int, Any]
    total_pages: Union[int, Any]
    page_size: Union[int, Any]
    total_items: Union[int, Any]
