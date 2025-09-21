"""Constants for the REST generator package"""

# Default paths and directories
DEFAULT_SWAGGER_PATH = "swagger.json"
DEFAULT_OUTPUT_DIR = "rest_clients"
FACADE_FILENAME = "facade.py"
APP_FACADE_FILENAME = "api_facade.py"

# Template names
CLIENT_TEMPLATE = "client_template.j2"
FACADE_TEMPLATE = "facade_template.j2"
APP_FACADE_TEMPLATE = "app_facade.j2"

# HTTP content types
CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_MULTIPART = "multipart/form-data"
CONTENT_TYPE_PDF = "application/pdf"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_TEXT_PLAIN = "text/plain"

# HTTP status codes for success responses
SUCCESS_STATUS_PREFIXES = ("2",)

# Supported HTTP methods
SUPPORTED_HTTP_METHODS = ["get", "post", "put", "patch", "delete"]

# Default tag for endpoints without tags
DEFAULT_TAG = "default"

# OpenAPI primitive type mappings
OPENAPI_TYPE_MAPPING = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "object": "Dict[str, Any]",
    "any": "Any",
}

# Python primitive types
PRIMITIVE_TYPES = {"str", "int", "float", "bool", "Any"}