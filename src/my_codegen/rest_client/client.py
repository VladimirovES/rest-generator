from typing import Union, Dict, List, Optional, Any
from http import HTTPStatus

from my_codegen.utils.base_url import ConfigUrl
from my_codegen.rest_client.proccesor import RequestHandler


class ApiClient:
    def __init__(
            self, auth_token: Optional[str] = None,
            base_url: Optional[str] = None
    ):
        self.base_url = base_url if base_url else ConfigUrl.get_base_url()
        self.auth_token = auth_token
        self._request_handler = RequestHandler(auth_token)

    def _send_request(
            self,
            method: str,
            path: str,
            payload: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            files: Optional[Dict] = None,
            data: Optional[Union[bytes, str]] = None,
            expected_status: Optional[HTTPStatus] = None,
            **kwargs,
    ) -> Union[Dict, List, bytes, None]:
        formatted_path = path.format(**kwargs)
        url = f"{self.base_url}{formatted_path}"

        request = self._request_handler.prepare_request(
            method, url, payload, headers, params, files, data
        )
        response = self._request_handler.send_request(request, path)

        if response.status_code != expected_status.value:
            assert response.status_code == expected_status.value, \
                f"Status code expected {expected_status.value}, got {response.status_code}"

        return self._request_handler.process_response(response)

    def get(
            self,
            path: str,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            expected_status: HTTPStatus = HTTPStatus.OK,
            **kwargs,
    ) -> Union[Dict, List]:
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
            headers: Optional[Dict] = None,
            files: Optional[Dict] = None,
            expected_status: HTTPStatus = HTTPStatus.CREATED,
            **kwargs,
    ) -> Union[Dict, List]:
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
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            files: Optional[Dict] = None,
            expected_status: HTTPStatus = HTTPStatus.OK,
            **kwargs,
    ) -> Union[Dict, List]:
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
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            expected_status: HTTPStatus = HTTPStatus.OK,
            **kwargs,
    ) -> Union[Dict, List]:
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
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            payload: Optional[Any] = None,
            expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
            **kwargs,
    ) -> Union[Dict, List]:
        return self._send_request(
            "DELETE",
            path,
            headers=headers,
            params=params,
            payload=payload,
            expected_status=expected_status,
            **kwargs,
        )