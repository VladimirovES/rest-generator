import re
from typing import Dict, Any, List, Optional
from http import HTTPStatus

from codegen.data_models import Endpoint, Parameter
from swagger.swagger_models import (
    SwaggerSpec,
    SwaggerOperation,
    SwaggerRequestBody,
    SwaggerResponse,
    SwaggerParameter,
)
from constants import (
    SUPPORTED_HTTP_METHODS,
    DEFAULT_TAG,
    CONTENT_TYPE_JSON,
    CONTENT_TYPE_MULTIPART,
    CONTENT_TYPE_OCTET_STREAM,
    CONTENT_TYPE_TEXT_PLAIN,
    SUCCESS_STATUS_PREFIXES,
    OPENAPI_TYPE_MAPPING,
)


class SwaggerProcessor:
    def __init__(self, swagger_spec: SwaggerSpec):
        self.swagger_spec = swagger_spec

    def extract_endpoints(self) -> List[Endpoint]:
        endpoints = []

        for path_str, path_obj in self.swagger_spec.paths.items():
            methods = {
                method: getattr(path_obj, method, None)
                for method in SUPPORTED_HTTP_METHODS
            }

            for http_method, operation in methods.items():
                if operation is None:
                    continue

                for tag in operation.tags or [DEFAULT_TAG]:
                    endpoint = self._create_endpoint(
                        path_str, http_method, operation, tag
                    )
                    endpoints.append(endpoint)

        return endpoints

    def _create_endpoint(
            self, path: str, http_method: str, operation: SwaggerOperation, tag: str
    ) -> Endpoint:

        expected_status, return_type = self._extract_response_info(operation.responses)

        return Endpoint(
            tag=tag,
            name=self._determine_method_name(http_method, path, operation),
            http_method=http_method.upper(),
            path=path,
            path_params=self._extract_parameters(operation.parameters, "path"),
            query_params=self._extract_parameters(operation.parameters, "query"),
            payload_type=self._extract_payload_type(operation.requestBody),
            expected_status=expected_status,
            return_type=return_type,
            description=operation.description or "",
            summary=operation.summary or "",
        )

    def extract_imports(self) -> List[str]:
        if not self.swagger_spec.components:
            return []
        return [
            self._remove_underscores(name)
            for name in self.swagger_spec.components.schemas.keys()
        ]

    # Private helper methods
    @staticmethod
    def _remove_underscores(name: str) -> str:
        segments = name.split("_")
        cleaned_segments = []
        for seg in segments:
            seg = seg.strip()
            if not seg:
                continue
            if re.match(r"^[A-Z][a-zA-Z0-9]*$", seg):
                cleaned_segments.append(seg)
            else:
                cleaned_segments.append(seg.capitalize())
        return "".join(cleaned_segments)

    def _extract_payload_type(self, request_body: Optional[SwaggerRequestBody]) -> str:
        if not request_body:
            return None

        content = request_body.content

        for ctype_key in (CONTENT_TYPE_JSON, CONTENT_TYPE_MULTIPART):
            if ctype_key in content:
                schema = content[ctype_key].get("schema", {})
                return self._map_openapi_type_to_python(schema)
        return None

    def _extract_response_info(
            self, responses: Dict[str, SwaggerResponse]
    ) -> tuple[str, str]:
        expected_status = "OK"
        return_type = "Any"

        for status_code, response_obj in responses.items():
            if any(status_code.startswith(prefix) for prefix in SUCCESS_STATUS_PREFIXES):
                expected_status = self._get_http_status_enum(status_code)

                resp_content = response_obj.content

                if CONTENT_TYPE_JSON in resp_content:
                    schema = resp_content[CONTENT_TYPE_JSON].get("schema", {})
                    return_type = self._map_openapi_type_to_python(schema)
                elif CONTENT_TYPE_OCTET_STREAM in resp_content:
                    return_type = "bytes"
                elif CONTENT_TYPE_TEXT_PLAIN in resp_content:
                    return_type = "str"
                break

        return (expected_status, return_type)

    @staticmethod
    def _get_http_status_enum(status_code: str) -> str:
        try:
            return HTTPStatus(int(status_code)).name
        except ValueError:
            return "OK"

    def _map_openapi_type_to_python(self, schema: Dict[str, Any]) -> str:
        if "$ref" in schema:
            raw_name = schema["$ref"].split("/")[-1]
            return self._remove_underscores(raw_name)

        openapi_type = schema.get("type", "Any")
        if openapi_type == "array":
            items = schema.get("items", {})
            return f"List[{self._map_openapi_type_to_python(items)}]"

        return OPENAPI_TYPE_MAPPING.get(openapi_type, "Any")

    def _extract_parameters(
            self, parameters: List[SwaggerParameter], location: str
    ) -> List[Parameter]:
        result = []
        for param in parameters:
            if param.in_ == location:
                result.append(
                    Parameter(
                        name=param.name,
                        type=self._map_openapi_type_to_python(param.schema_ or {}),
                        required=param.required,
                    )
                )
        return result

    def _determine_method_name(
            self, http_method: str, path: str, operation: SwaggerOperation
    ) -> str:
        if operation.summary:
            raw_name = operation.summary
        elif operation.operationId:
            raw_name = operation.operationId
        else:
            raw_name = f"{http_method}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}"
        return re.sub(r"[^a-zA-Z0-9]+", "_", raw_name.strip().lower()).strip("_")
