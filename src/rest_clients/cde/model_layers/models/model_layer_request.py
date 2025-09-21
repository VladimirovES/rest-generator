"""Generated model: ModelLayerRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Union


class ModelLayerRequest(BaseConfigModel):
    filters: FiltersModelLayerRequest
    page: Union[int, Any] = 1
    page_size: Union[int, Any] = 10
