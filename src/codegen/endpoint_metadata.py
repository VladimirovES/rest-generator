"""Shared helpers for endpoint metadata used in test and assert generation."""

from dataclasses import dataclass
from typing import List, Optional

from codegen.data_models import Endpoint
from utils.naming import to_snake_case


@dataclass
class EndpointInfo:
    """Normalized information about a generated client endpoint."""

    method_name: str
    http_method: str
    path: str
    description: str
    endpoint: Optional[Endpoint]


def build_endpoint_info(endpoints: List[Endpoint]) -> List[EndpointInfo]:
    """Create a stable, unique list of endpoint descriptors for a module."""

    seen_names = set()
    infos: List[EndpointInfo] = []

    for endpoint in endpoints:
        base_name = to_snake_case(endpoint.name) or "endpoint"
        method_name = base_name

        # Ensure method names are unique within the module
        if method_name in seen_names:
            suffix = 2
            while f"{base_name}_{suffix}" in seen_names:
                suffix += 1
            method_name = f"{base_name}_{suffix}"

        seen_names.add(method_name)

        description = endpoint.summary or endpoint.description or endpoint.name

        infos.append(
            EndpointInfo(
                method_name=method_name,
                http_method=endpoint.http_method.upper(),
                path=endpoint.path,
                description=description,
                endpoint=endpoint,
            )
        )

    return infos
