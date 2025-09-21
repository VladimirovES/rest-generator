"""Generated model: RoomPassportResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Union


class RoomPassportResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    number: str
    height: Union[str, Any]
    content: List[ContentRoomPassportSchema] = []
