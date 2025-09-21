"""Generated model: ReportPage."""

from pydantic import BaseModel
from typing import Any, Dict, List, Union


class ReportPage(BaseModel):
    results: List[Any]
    previous: Union[int, Any]
    count: Union[int, Any]
    next: Union[int, Any]
    meta: Union[Dict[str, Any], Any]
