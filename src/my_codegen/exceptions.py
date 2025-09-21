"""Custom exceptions for the REST generator package."""

from typing import Optional, Any
from http import HTTPStatus


class RestGeneratorError(Exception):
    """Base exception for rest generator."""

    def __init__(self, message: str, details: Optional[Any] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class SwaggerProcessingError(RestGeneratorError):
    """Error during Swagger/OpenAPI specification processing."""
    pass


class CodeGenerationError(RestGeneratorError):
    """Error during code generation."""
    pass


class ApiClientError(RestGeneratorError):
    """Base exception for API client errors."""
    pass


class HttpError(ApiClientError):
    """HTTP request/response error."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Any] = None,
        url: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data
        self.url = url

    def __str__(self) -> str:
        base_msg = self.message
        if self.status_code:
            base_msg += f" (Status: {self.status_code})"
        if self.url:
            base_msg += f" (URL: {self.url})"
        return base_msg


class UnexpectedStatusCodeError(HttpError):
    """Raised when API response has unexpected status code."""

    def __init__(
        self,
        expected: HTTPStatus,
        actual: int,
        url: str,
        response_data: Optional[Any] = None
    ) -> None:
        message = f"Expected status {expected.value}, got {actual}"
        super().__init__(message, actual, response_data, url)
        self.expected = expected
        self.actual = actual


class RequestPreparationError(ApiClientError):
    """Error during request preparation."""
    pass


class ResponseProcessingError(ApiClientError):
    """Error during response processing."""
    pass


class ConfigurationError(RestGeneratorError):
    """Configuration related error."""
    pass