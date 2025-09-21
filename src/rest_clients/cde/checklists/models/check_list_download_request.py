"""Generated model: CheckListDownloadRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class CheckListDownloadRequest(BaseConfigModel):
    type: List[CheckListDownloadType]
