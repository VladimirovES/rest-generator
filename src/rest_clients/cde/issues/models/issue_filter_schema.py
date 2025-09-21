"""Generated model: IssueFilterSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List, Optional, Union


class IssueFilterSchema(BaseConfigModel):
    statuses: Optional[Union[List[str], Any]] = None
    sort: Optional[Union[List[str], Any]] = None
