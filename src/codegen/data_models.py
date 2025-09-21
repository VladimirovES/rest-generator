from dataclasses import dataclass, field
from typing import List, Optional

from constants import PRIMITIVE_TYPES


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
    summary: str = ""


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


class ParameterBuilder:
    """Builds parameter lists for methods"""

    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    def build_required_params(self) -> List[str]:
        """Build required parameters"""
        params = []
        params.extend(self._build_path_params())
        params.extend(self._build_required_query_params())

        if self._is_payload_required():
            params.append(f"payload: {self.endpoint.payload_type}")

        return params

    def build_optional_params(self) -> List[str]:
        """Build optional parameters"""
        params = []
        params.extend(self._build_optional_query_params())

        if self.endpoint.http_method == "GET":
            params.append("params: Optional[Dict[str, Any]] = None")
        elif not self._is_payload_required():
            params.append("payload: Optional[Any] = None")

        return params

    def _build_path_params(self) -> List[str]:
        return [f"{p.name}: {p.type}" for p in self.endpoint.path_params]

    def _build_required_query_params(self) -> List[str]:
        return [f"{p.name}: {p.type}" for p in self.endpoint.query_params if p.required]

    def _build_optional_query_params(self) -> List[str]:
        return [
            f"{p.name}: Optional[{p.type}] = None"
            for p in self.endpoint.query_params
            if not p.required
        ]

    def _is_payload_required(self) -> bool:
        return (
            self.endpoint.http_method != "GET"
            and self.endpoint.payload_type
            and self.endpoint.payload_type != "Any"
        )

class HttpCallBuilder:
    """Builds HTTP call parts"""

    def __init__(self, endpoint: Endpoint, service_path: str = ""):
        self.endpoint = endpoint
        self.service_path = service_path

    def build_http_call(self) -> str:
        """Generate HTTP call"""
        if self.endpoint.http_method == "GET":
            return self._build_get_call()
        else:
            return self._build_post_call()

    def build_path_assignment(self) -> str:
        """Generate path variable assignment"""
        full_path = f"{self.service_path}{self.endpoint.path}"
        return full_path

    def _build_get_call(self) -> str:
        """GET request"""
        params_dict = self._build_query_params_dict(include_params=True)
        method = self.endpoint.http_method.lower()

        return f"""r_json = self._client.{method}(
            path=path,
            params={params_dict},
            headers=headers,
            expected_status=expected_status
        )"""
    
    def _build_post_call(self) -> str:
        """POST/PUT/PATCH/DELETE request"""
        method = self.endpoint.http_method.lower()
        call_parts = ["path=path"]

        payload_parts = self._build_payload_parts()
        if payload_parts:
            call_parts.extend(payload_parts)

        if self.endpoint.query_params:
            params_dict = self._build_query_params_dict(include_params=False)
            call_parts.append(f"params={params_dict}")

        call_parts.extend(["headers=headers", "expected_status=expected_status"])

        joined_parts = ",\n            ".join(call_parts)
        return f"""r_json = self._client.{method}(
            {joined_parts}
        )"""

    def _build_payload_parts(self) -> List[str]:
        """Build payload parts"""
        if not self.endpoint.payload_type:
            return []

        if self.endpoint.payload_type != "Any":
            return ["payload=payload"]

        return []

    def _build_query_params_dict(self, include_params: bool = False) -> str:
        """Build query parameters dictionary"""
        params_dict = "{"
        for param in self.endpoint.query_params:
            params_dict += f"'{param.name}': {param.name}, "

        if include_params:
            params_dict += "**(params or {})"

        params_dict += "}"
        return params_dict


class ReturnStatementBuilder:
    """Builds return statements"""

    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint

    def build_return_statement(self) -> str:
        """Generate return statement"""
        if self.endpoint.return_type == "Any":
            return "return r_json"

        condition = (
            f"if expected_status == HTTPStatus.{self.endpoint.expected_status} else r_json"
        )

        if self.endpoint.return_type.startswith("List["):
            return self._build_list_return(condition)
        elif self._is_primitive_type():
            return self._build_primitive_return(condition)
        else:
            return self._build_model_return(condition)

    def _build_list_return(self, condition: str) -> str:
        """List[Model] return"""
        inner_type = self.endpoint.return_type[5:-1]

        if inner_type in PRIMITIVE_TYPES:
            return f"return [item for item in r_json] {condition}"
        else:
            return f"return [{inner_type}(**item) for item in r_json] {condition}"

    def _build_primitive_return(self, condition: str) -> str:
        """Primitive type return"""
        return f"return {self.endpoint.return_type}(r_json) {condition}"

    def _build_model_return(self, condition: str) -> str:
        """Model return"""
        return f"return {self.endpoint.return_type}(**r_json) {condition}"

    def _is_primitive_type(self) -> bool:
        return self.endpoint.return_type in PRIMITIVE_TYPES


@dataclass
class MethodContext:
    """Class for rendering content in templates"""

    name: str
    description: str
    summary: str
    path: str
    return_type: str
    expected_status: str
    required_params: List[str]
    optional_params: List[str]
    path_assignment: str
    method:str
    http_call: str
    return_statement: str

    @classmethod
    def from_endpoint(cls, endpoint: Endpoint, service_path: str = "") -> "MethodContext":
        """Convert Endpoint to MethodContext"""

        param_builder = ParameterBuilder(endpoint)
        http_builder = HttpCallBuilder(endpoint, service_path)
        return_builder = ReturnStatementBuilder(endpoint)

        return cls(
            name=endpoint.name,
            description=endpoint.description,
            summary=endpoint.summary,
            path=endpoint.path,
            method = endpoint.http_method.upper(),
            return_type=endpoint.return_type,
            expected_status=endpoint.expected_status,
            required_params=param_builder.build_required_params(),
            optional_params=param_builder.build_optional_params(),
            path_assignment=http_builder.build_path_assignment(),
            http_call=http_builder.build_http_call(),
            return_statement=return_builder.build_return_statement(),
        )