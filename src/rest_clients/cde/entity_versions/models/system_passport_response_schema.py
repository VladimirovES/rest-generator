"""Generated model: SystemPassportResponseSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import Union


class SystemPassportResponseSchema(BaseConfigModel):
    oid: UUID
    name: str
    classification: Union[str, Any]
    type: str
    flow: Union[str, Any]
    serviced_rooms_param: Union[str, Any]
    equip_location_param: Union[str, Any]
