"""Generated model: ReportSearchField."""

from pydantic import BaseModel
from typing import Any, List, Optional, Union


class ReportSearchField(BaseModel):
    name: str
    data: Optional[Union[List[str], Any]] = None
