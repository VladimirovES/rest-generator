"""Generated model: ModelLayerFilesResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class ModelLayerFilesResponse(BaseConfigModel):
    files: List[ModelLayerFileResponse]
