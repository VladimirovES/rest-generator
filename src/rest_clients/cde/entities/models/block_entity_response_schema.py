"""Generated model: BlockEntityResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Union


class BlockEntityResponseSchema(BaseConfigModel):
    user: UserResponseSchema
    unlock_time: Union[int, float]
