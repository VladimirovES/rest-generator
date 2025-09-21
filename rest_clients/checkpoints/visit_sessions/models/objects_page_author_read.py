"""Generated model: ObjectsPage_AuthorRead_."""

from pydantic import BaseModel
from typing import Any, List, Union
from . import AuthorRead


class ObjectsPage_AuthorRead_(BaseModel):
    objects: List[AuthorRead]
    current_page: Union[int, Any]
    total_pages: Union[int, Any]
    page_size: Union[int, Any]
    total_items: Union[int, Any]
