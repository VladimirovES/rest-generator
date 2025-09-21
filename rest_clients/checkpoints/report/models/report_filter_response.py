"""Generated model: ReportFilterResponse."""

from pydantic import BaseModel


class ReportFilterResponse(BaseModel):
    name: str
    text: str
    is_visible: bool
