"""Generated model: ObjectsPage_VisitSessionSearchResponse_."""

from pydantic import BaseModel
from typing import Any, List, Union
from . import VisitSessionSearchResponse


class ObjectsPage_VisitSessionSearchResponse_(BaseModel):
    objects: List[VisitSessionSearchResponse]
    current_page: Union[int, Any]
    total_pages: Union[int, Any]
    page_size: Union[int, Any]
    total_items: Union[int, Any]
