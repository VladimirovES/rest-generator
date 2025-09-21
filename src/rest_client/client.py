"""API client for making HTTP requests with authentication and error handling."""

from typing import Union, Dict, List, Optional, Any
from http import HTTPStatus

from rest_client.base_url import ConfigUrl
from rest_client.processor import RequestHandler
from exceptions import UnexpectedStatusCodeError, ApiClientError


class ApiClient:
    """HTTP API client with authentication and request handling capabilities.

    This client provides a high-level interface for making HTTP requests
    with automatic authentication, retries, and response processing.

    Args:
        auth_token: Optional authentication token for API requests
        base_url: Optional base URL for API endpoints
    """

    def __init__(self, auth_token: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self.base_url = base_url or ConfigUrl.get_base_url()
        self.auth_token = auth_token
        self._request_handler = RequestHandler(auth_token)

    def _send_request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        data: Optional[Union[bytes, str]] = None,
        expected_status: Optional[HTTPStatus] = None,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], List[Any], bytes, None]:
        """Send HTTP request and handle response.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API endpoint path with optional format placeholders
            payload: JSON payload for request body
            headers: Additional HTTP headers
            params: URL query parameters
            files: Files for multipart upload
            data: Raw request body data
            expected_status: Expected HTTP status code
            **kwargs: Path format parameters

        Returns:
            Parsed response data or raw bytes

        Raises:
            UnexpectedStatusCodeError: When response status doesn't match expected
            ApiClientError: For other API-related errors
        """
        formatted_path = path.format(**kwargs)
        url = f"{self.base_url}{formatted_path}"

        request = self._request_handler.prepare_request(
            method, url, payload, headers, params, files, data
        )
        response = self._request_handler.send_request(request, path)

        if response.status_code != expected_status.value:
            raise UnexpectedStatusCodeError(
                expected=expected_status,
                actual=response.status_code,
                url=url,
                response_data=self._request_handler.process_response(response)
            )

        return self._request_handler.process_response(response)

    def get(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], List[Any]]:
        """Send GET request.

        Args:
            path: API endpoint path
            headers: Additional HTTP headers
            params: URL query parameters
            expected_status: Expected HTTP status code
            **kwargs: Path format parameters

        Returns:
            Response data as dict or list
        """
        return self._send_request(
            "GET",
            path,
            params=params,
            headers=headers,
            expected_status=expected_status,
            **kwargs,
        )

    def post(
        self,
        path: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], List[Any]]:
        """Send POST request.

        Args:
            path: API endpoint path
            payload: Request payload data
            headers: Additional HTTP headers
            files: Files for multipart upload
            expected_status: Expected HTTP status code
            **kwargs: Path format parameters

        Returns:
            Response data as dict or list
        """
        return self._send_request(
            "POST",
            path,
            payload=payload,
            files=files,
            headers=headers,
            expected_status=expected_status,
            **kwargs,
        )

    def put(
        self,
        path: str = "",
        payload: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Any]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], List[Any]]:
        return self._send_request(
            "PUT",
            path,
            payload=payload,
            params=params,
            headers=headers,
            files=files,
            expected_status=expected_status,
            **kwargs,
        )

    def patch(
        self,
        path: str,
        payload: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], List[Any]]:
        return self._send_request(
            "PATCH",
            path,
            payload=payload,
            params=params,
            headers=headers,
            expected_status=expected_status,
            **kwargs,
        )

    def delete(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Any] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], List[Any]]:
        return self._send_request(
            "DELETE",
            path,
            headers=headers,
            params=params,
            payload=payload,
            expected_status=expected_status,
            **kwargs,
        )


class NonAuthorizedClient(ApiClient):
    """API client without authentication.

    Use this client for public endpoints that don't require authentication.

    Args:
        base_url: Optional base URL for API endpoints
    """

    def __init__(self, base_url: Optional[str] = None) -> None:
        super().__init__(auth_token=None, base_url=base_url)
        self._request_handler = RequestHandler()


class AuthorizedClient(ApiClient):
    """API client with required authentication.

    Use this client for endpoints that require authentication.

    Args:
        auth_token: Authentication token (required)
        base_url: Optional base URL for API endpoints
    """

    def __init__(self, auth_token: str, base_url: Optional[str] = None) -> None:
        super().__init__(auth_token=auth_token, base_url=base_url)
        self._request_handler = RequestHandler(auth_token)
