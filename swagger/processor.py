import re
from typing import Dict, Any, List
from http import HTTPStatus

from codegen.data_models import Endpoint, Parameter
from utils.common import remove_underscores

class SwaggerProcessor:
    def __init__(self, swagger: Dict[str, Any]):
        self.swagger = swagger

    def extract_endpoints(self) -> List[Endpoint]:
        endpoints: List[Endpoint] = []
        paths = self.swagger.get('paths', {})

        for path, methods in paths.items():
            for http_method, details in methods.items():
                tags = details.get('tags', ['default'])
                for tag in tags:
                    method_name = self._determine_method_name(http_method, path, details)
                    description = details.get('description', details.get('summary', ''))

                    parameters = details.get('parameters', [])
                    path_params = self._extract_parameters(parameters, 'path')
                    query_params = self._extract_parameters(parameters, 'query')

                    request_body = details.get('requestBody', {})
                    payload_type = self._extract_payload_type(request_body)

                    responses = details.get('responses', {})
                    expected_status, return_type = self._extract_response_info(responses)

                    endpoints.append(Endpoint(
                        tag=tag,
                        name=method_name,
                        http_method=http_method.upper(),
                        path=path,
                        path_params=path_params,
                        query_params=query_params,
                        payload_type=payload_type,
                        expected_status=expected_status,
                        return_type=return_type,
                        description=description
                    ))
        return endpoints

    def extract_imports(self) -> List[str]:
        components = self.swagger.get('components', {})
        schemas = components.get('schemas', {})
        return [remove_underscores(name) for name in schemas.keys()]

    # -- private helpers --

    def _extract_payload_type(self, request_body: Dict[str, Any]) -> str:
        if not request_body:
            return None
        content = request_body.get('content', {})
        for ctype_key in ('application/json', 'multipart/form-data'):
            if ctype_key in content:
                schema = content[ctype_key].get('schema', {})
                return self._map_openapi_type_to_python(schema)
        return None

    def _extract_response_info(self, responses: Dict[str, Any]) -> (str, str):
        expected_status = 'OK'
        return_type = 'Any'
        for status_code, response_obj in responses.items():
            if status_code.startswith('2'):
                expected_status = self._get_http_status_enum(status_code)
                resp_content = response_obj.get('content', {})
                if 'application/json' in resp_content:
                    schema = resp_content['application/json'].get('schema', {})
                    return_type = self._map_openapi_type_to_python(schema)
                elif 'application/octet-stream' in resp_content:
                    return_type = 'bytes'
                elif 'text/plain' in resp_content:
                    return_type = 'str'
                break
        return (expected_status, return_type)

    @staticmethod
    def _get_http_status_enum(status_code: str) -> str:
        try:
            return HTTPStatus(int(status_code)).name
        except ValueError:
            return 'OK'

    def _map_openapi_type_to_python(self, schema: Dict[str, Any]) -> str:
        if '$ref' in schema:
            raw_name = schema['$ref'].split('/')[-1]
            return remove_underscores(raw_name)

        openapi_type = schema.get('type', 'Any')
        if openapi_type == 'array':
            items = schema.get('items', {})
            return f"List[{self._map_openapi_type_to_python(items)}]"

        type_mapping = {
            'string': 'str',
            'integer': 'int',
            'number': 'float',
            'boolean': 'bool',
            'object': 'Dict[str, Any]',
            'any': 'Any'
        }
        return type_mapping.get(openapi_type, 'Any')

    def _extract_parameters(self, parameters: List[Dict[str, Any]], location: str) -> List[Parameter]:
        result = []
        for param in parameters:
            if param.get('in') == location:
                schema = param.get('schema', {})
                result.append(
                    Parameter(
                        name=param.get('name'),
                        type=self._map_openapi_type_to_python(schema),
                        required=param.get('required', False)
                    )
                )
        return result

    def _determine_method_name(self, http_method: str, path: str, details: Dict[str, Any]) -> str:
        summary = details.get('summary', '')
        operation_id = details.get('operationId', '')
        if summary:
            raw_name = summary
        elif operation_id:
            raw_name = operation_id
        else:
            raw_name = f"{http_method}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}"
        return re.sub(r'[^a-zA-Z0-9]+', '_', raw_name.strip().lower()).strip('_')
