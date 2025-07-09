import mimetypes
import os
import pprint
from enum import Enum
from typing import Union, Dict, List, Optional, Any

from pydantic import BaseModel

import allure
import requests
from http import HTTPStatus

from dotenv import load_dotenv

from requests.adapters import HTTPAdapter, Retry

import json
import uuid

from my_codegen.utils.base_url import BaseUrlSingleton
from my_codegen.utils.logger import allure_report, ApiRequestError, logger

from my_codegen.utils.report_utils import Reporter

load_dotenv()


class RequestHandler:
    def __init__(self, auth_token: Optional[str] = None):
        self.auth_token = auth_token
        self.session = requests.Session()
        self._configure_retries()

    def _configure_retries(self):
        retries = Retry(
            total=10,
            backoff_factor=2,
            status_forcelist=[502, 504],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _add_authorization_header(
            self, headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, str]:
        headers = headers or {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def _process_payload(self, payload: Any) -> Optional[str]:
        """
        Обрабатывает payload разных типов и конвертирует в JSON строку
        """
        if payload is None:
            return None

        if isinstance(payload, BaseModel):
            return payload.model_dump_json()

        if isinstance(payload, list) and payload and isinstance(payload[0], BaseModel):
            from pydantic import RootModel
            ListModel = RootModel[List[type(payload[0])]]
            return ListModel(payload).model_dump_json()

    def prepare_request(
            self,
            method: str,
            url: str,
            payload: Optional[Any] = None,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            files: Optional[Dict] = None,
            data: Optional[Union[bytes, str]] = None
    ) -> requests.PreparedRequest:

        headers = self._add_authorization_header(headers)

        if files or data is not None:
            pass
        elif "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        if data is None and payload is not None and not files:
            data = self._process_payload(payload)

        request = requests.Request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            files=files,
        )
        return request.prepare()

    def send_request(
            self,
            prepared_request: requests.PreparedRequest, path: str
    ) -> requests.Response:
        response = self.session.send(prepared_request)
        return response

    def validate_response(
            self,
            response: requests.Response,
            expected_status: Optional[HTTPStatus],
            method: str,
            payload: Optional[Dict] = None,
    ):
        if expected_status and response.status_code != expected_status.value:
            raise ApiRequestError(response, expected_status, method, payload)

    def process_response(
            self, response: requests.Response
    ) -> Union[Dict, List, bytes, str, None]:
        try:
            if "application/pdf" in response.headers.get(
                    "Content-Type", ""
            ) or "bytes" in response.headers.get("Accept-Ranges", ""):
                return response.content
            if response.status_code == HTTPStatus.NO_CONTENT:
                return response.text
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return response.text


class ApiClient:
    def __init__(
            self, auth_token: Optional[str] = None, base_url: Optional[str] = None
    ):
        self.base_url = base_url if base_url else BaseUrlSingleton.get_base_url()
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

        prepared_request = self._request_handler.prepare_request(
            method, url, payload, headers, params, files, data
        )
        response = self._request_handler.send_request(prepared_request, path)

        self._request_handler.validate_response(
            response, expected_status, method, payload or params
        )
        logger.info(f'{response.status_code} | {method} | {formatted_path}')

        return self._request_handler.process_response(response)

    def _get(
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

    def _post(
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

    def _put(
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

    def _patch(
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

    def _delete(
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


class StorageS3(ApiClient):
    def __init__(self, url: str):
        super().__init__(auth_token=None, base_url=url)
        self.base_url = url

    def upload(self, file_path: str):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        with open(file_path, "rb") as f:
            file_content = f.read()
            headers = {
                "Content-Type": mime_type,
                "Content-Length": str(os.path.getsize(file_path))
            }
            return self._put(
                path="",
                payload=None,  # Important: don't send as JSON payload
                headers=headers,
                files=None,  # Don't use files parameter for S3 direct upload
                data=file_content,  # Send raw file content
                expected_status=HTTPStatus.OK
            )

    def download(self):
        return self._get(path="")
