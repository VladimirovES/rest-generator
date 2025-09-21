"""Generated model: ReportSearchData."""

from pydantic import BaseModel
from typing import Any, List, Union
from . import ReportSearchField


class ReportSearchData(BaseModel):
    fields: Union[List[ReportSearchField], Any] = []
