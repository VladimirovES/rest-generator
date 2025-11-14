"""Constants for the REST generator package"""

DEFAULT_SWAGGER_PATH = "swagger.json"
DEFAULT_OUTPUT_DIR = "rest_clients"
DEFAULT_TESTS_DIR = "tests"
FACADE_FILENAME = "facade.py"
APP_FACADE_FILENAME = "api_facade.py"

CLIENT_TEMPLATE = "client_template.j2"
FACADE_TEMPLATE = "facade_template.j2"
APP_FACADE_TEMPLATE = "app_facade.j2"

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_MULTIPART = "multipart/form-data"
CONTENT_TYPE_PDF = "application/pdf"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_TEXT_PLAIN = "text/plain"

SUCCESS_STATUS_PREFIXES = ("2",)

SUPPORTED_HTTP_METHODS = ["get", "post", "put", "patch", "delete"]

DEFAULT_TAG = "default"

OPENAPI_TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "object": "Dict[str, Any]",
    "any": "Any",
}

PRIMITIVE_TYPES = {"str", "int", "float", "bool", "Any"}
