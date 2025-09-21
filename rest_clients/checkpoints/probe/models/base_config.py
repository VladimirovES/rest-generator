"""Base configuration for Pydantic models."""

from pydantic import BaseModel


class BaseConfigModel(BaseModel):
    """Base model class with common configuration."""

    class Config:
        extra = "forbid"
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True
