"""REST API client generator from Swagger/OpenAPI specifications."""

__version__ = "1.2.0"
__author__ = "Vladimirov Evgeniy"
__email__ = "evgeniy.vladimirov@example.com"

from main import RestGenerator
from exceptions import (
    RestGeneratorError,
    SwaggerProcessingError,
    CodeGenerationError,
    ApiClientError,
    HttpError,
    UnexpectedStatusCodeError,
)

__all__ = [
    "RestGenerator",
    "RestGeneratorError",
    "SwaggerProcessingError",
    "CodeGenerationError",
    "ApiClientError",
    "HttpError",
    "UnexpectedStatusCodeError",
]