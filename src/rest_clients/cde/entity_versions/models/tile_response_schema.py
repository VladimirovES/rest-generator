"""Generated model: TileResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import Any, Dict, List, Optional


class TileResponseSchema(BaseConfigModel):
    json_files: Optional[List[Dict[str, Any]]] = None
    tiles: Optional[Dict[str, Any]] = None
