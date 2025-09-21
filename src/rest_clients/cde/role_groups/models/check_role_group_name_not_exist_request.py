"""Generated model: CheckRoleGroupNameNotExistRequest."""

from pydantic_utils.pydantic_config import BaseConfigModel
from pydantic import Field


class CheckRoleGroupNameNotExistRequest(BaseConfigModel):
    name: str = Field(min_length=1, max_length=50)
