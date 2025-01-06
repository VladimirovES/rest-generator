from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Parameter:
    name: str
    type: str
    required: bool = False


@dataclass
class Endpoint:
    tag: str
    name: str
    http_method: str
    path: str
    path_params: List[Parameter] = field(default_factory=list)
    query_params: List[Parameter] = field(default_factory=list)
    payload_type: Optional[str] = None
    expected_status: str = "OK"
    return_type: str = "Any"
    description: str = ""

    @property
    def sanitized_path(self) -> str:
        return self.path if self.path.startswith("/") else f"/{self.path}"

    @property
    def method_parameters(self) -> List[str]:
        return [f"{p.name}: {p.type}" for p in self.path_params if p.required]


@dataclass
class SubPath:
    name: str
    path: str
