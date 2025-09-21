"""Generated model: Categories."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class Categories(BaseConfigModel):
    categories: List[Category]
