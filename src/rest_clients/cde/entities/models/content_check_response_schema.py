"""Generated model: ContentCheckResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Optional, Union


class ContentCheckResponseSchema(BaseConfigModel):
    type: EntityType
    validation: ContentValidationType
    error: Optional[Union[ContentErrorSchema, Any]] = None
