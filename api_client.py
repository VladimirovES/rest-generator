import mimetypes
import os
import pprint
from datetime import datetime
from enum import Enum
from typing import Union, Dict, List, Optional

import allure
import requests
from http import HTTPStatus
# from decouple import config

# from logging_config import allure_response_and_payload

from requests.adapters import HTTPAdapter, Retry

import json
import uuid


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        # if isinstance(obj, datetime):
        #     return obj.isoformat()
        if isinstance(obj, Enum):
            return obj.value

        return super().default(obj)


class RequestHandler:
    def __init__(self, base_url: str,
                 auth_token: Optional[str] = None):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = requests.Session()
        self._configure_retries()

    def _configure_retries(self):
        retries = Retry(
            total=10,
            backoff_factor=2,
            status_forcelist=[502, 504],
            raise_on_status=False
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _add_authorization_header(self, headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        headers = headers or {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def prepare_request(self,
                        method: str,
                        url: str,
                        payload: Optional[Dict] = None,
                        headers: Optional[Dict] = None,
                        params: Optional[Dict] = None,
                        files: Optional[Dict] = None
                        ) -> requests.PreparedRequest:

        headers = self._add_authorization_header(headers)

        if "Content-Type" not in headers:
            if not files:
                headers["Content-Type"] = "application/json"

        if payload is not None and not files:
            data = json.dumps(payload, cls=UUIDEncoder)
        else:
            data = None

        request = requests.Request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            files=files
        )
        return request.prepare()

    def send_request(self,
                     prepared_request: requests.PreparedRequest,
                     path: str) -> requests.Response:
        response = self.session.send(prepared_request)
        with allure.step(f'{prepared_request.method}: {path}'):
            return response

    def validate_response(self, response: requests.Response, expected_status: Optional[HTTPStatus], method: str,
                          payload: Optional[Dict] = None):
        if expected_status and response.status_code != expected_status.value:
            response_text = response.text[:2000]
            payload_str = pprint.pformat(payload) if payload else ""
            error_message = (
                f"Expected status: {expected_status}, actual status: {response.status_code}.\n"
                f"Method: {method}\n"
                f"URL: {response.url}\n"
                f"response: {response_text},"
                f"headers: {response.request.headers}"
                f"payload: {payload_str}\n"
            )
            raise AssertionError(error_message)

    def process_response(self, response: requests.Response) -> Union[Dict, List, bytes, str, None]:
        try:
            if 'application/pdf' in response.headers.get('Content-Type', '') or 'bytes' in response.headers.get(
                    'Accept-Ranges', ''):
                return response.content
            if response.status_code == HTTPStatus.NO_CONTENT:
                return response.text
            return response.json()
        except requests.exceptions.JSONDecodeError:
            return response.text


class ApiClient:
    def __init__(self,
                 auth_token: Optional[str] = None,
                 base_url: Optional[str] = None,
                 use_versioned_api: Optional[bool] = True):
        self.url = base_url if base_url else 'BaseUrlSingleton.get_base_url()'
        self.base_url = f"{self.url}api{('VERSION_API')}" if use_versioned_api else f"{self.url}"
        self.auth_token = auth_token
        self.request_handler = RequestHandler(self.base_url, auth_token)

    def _send_request(self,
                      method: str,
                      path: str,
                      payload: Optional[Dict] = None,
                      headers: Optional[Dict] = None,
                      params: Optional[Dict] = None,
                      files: Optional[Dict] = None,
                      expected_status: Optional[HTTPStatus] = None,
                      **kwargs) -> Union[Dict, List, bytes, None]:
        formatted_path = path.format(**kwargs)

        url = f"{self.base_url}{formatted_path}"

        prepared_request = self.request_handler.prepare_request(method, url, payload, headers, params, files)
        response = self.request_handler.send_request(prepared_request, path)

        self.request_handler.validate_response(response, expected_status, method, payload or params)
        return self.request_handler.process_response(response)

    def get(self,
            path: str,
            headers: Optional[Dict] = None,
            params: Optional[Dict] = None,
            expected_status: HTTPStatus = HTTPStatus.OK,
            **kwargs) -> Union[Dict, List]:
        return self._send_request('GET', path,
                                  params=params,
                                  headers=headers,
                                  expected_status=expected_status,
                                  **kwargs)

    def post(self,
             path: str,
             payload: Optional[Union[Dict, List]] = None,
             headers: Optional[Dict] = None,
             files: Optional[Dict] = None,
             expected_status: HTTPStatus = HTTPStatus.CREATED,
             **kwargs) -> Union[Dict, List]:
        return self._send_request('POST',
                                  path,
                                  payload=payload,
                                  files=files,
                                  headers=headers,
                                  expected_status=expected_status,
                                  **kwargs)

    def put(self,
            path: str = '',
            payload: Optional[Dict] = None,
            params: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            files: Optional[Dict] = None,
            expected_status: HTTPStatus = HTTPStatus.OK,
            **kwargs) -> Union[Dict, List]:
        return self._send_request('PUT', path,
                                  payload=payload,
                                  params=params,
                                  headers=headers,
                                  files=files,
                                  expected_status=expected_status,
                                  **kwargs)

    def patch(self,
              path: str,
              payload: Optional[Dict] = None,
              params: Optional[Dict] = None,
              headers: Optional[Dict] = None,
              expected_status: HTTPStatus = HTTPStatus.OK,
              **kwargs) -> Union[Dict, List]:
        return self._send_request('PATCH', path,
                                  payload=payload,
                                  params=params,
                                  headers=headers,
                                  expected_status=expected_status,
                                  **kwargs)

    def delete(self,
               path: str,
               headers: Optional[Dict] = None,
               params: Optional[Dict] = None,
               payload: Optional[Dict, List] = None,
               expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
               **kwargs) -> Union[Dict, List]:
        return self._send_request('DELETE', path,
                                  headers=headers,
                                  params=params,
                                  payload=payload,
                                  expected_status=expected_status,
                                  **kwargs)


class ApiClientServices(ApiClient):
    def __init__(self, auth_token=None, base_url=None):
        super().__init__(auth_token=auth_token, base_url=base_url)
        self.base_url = self.url


class StorageS3(ApiClient):
    def __init__(self, url: str):
        super().__init__(auth_token=None, base_url=url)
        self.base_url = url

    def upload(self, file_path: str):
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, mime_type)}
            return self.put(files=files)

    def download(self):
        return self.get(path='')
