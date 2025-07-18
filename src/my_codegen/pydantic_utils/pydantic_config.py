from pydantic import BaseModel


class BaseConfigModel(BaseModel):
    class Config:
        extra = "forbid"
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True
