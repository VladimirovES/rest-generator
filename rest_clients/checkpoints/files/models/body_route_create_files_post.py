"""Generated model: Body_route_create_files_post."""

from pydantic import BaseModel


class Body_route_create_files_post(BaseModel):
    file: bytes
    """Вложения"""
