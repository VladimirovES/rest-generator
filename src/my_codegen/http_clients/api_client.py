import mimetypes
import os
import pprint
from enum import Enum
from typing import Union, Dict, List, Optional, Any

from pydantic import BaseModel, RootModel

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

import structlog
from curlify2 import Curlify

load_dotenv()


class Logging:
    def __init__(self) -> None:
        self.log = structlog.get_logger(__name__).bind(service="api")

    def log_request(self, method: str, url: str, **kwargs: Any) -> None:
        log = self.log.bind(event_id=str(uuid.uuid4()))
        json_data = kwargs.get("json")
        content = kwargs.get("content")
        data = kwargs.get("data")

        # Попробуем извлечь JSON из разных источников
        try:
            if content:
                json_data = json.loads(content)
            elif data and isinstance(data, str):
                json_data = json.loads(data)
        except json.JSONDecodeError:
            pass

        # Собираем все данные в один словарь
        request_info = {
            "event": "request",
            "method": method,
            "url": url
        }

        if kwargs.get("params"):
            request_info["params"] = kwargs.get("params")

        if kwargs.get("headers"):
            request_info["headers"] = kwargs.get("headers")

        if json_data:
            request_info["payload"] = json_data
        elif data:
            request_info["data"] = data

        # Форматированный JSON для вывода и Allure
        formatted_request = json.dumps(request_info, indent=2, ensure_ascii=False)
        print(formatted_request)

        # Allure attachment для запроса (только JSON данные)
        if json_data:
            allure.attach(
                json.dumps(json_data, indent=2, ensure_ascii=False),
                name=f"Request: {method} {url}",
                attachment_type=allure.attachment_type.JSON
            )

        msg = dict(
            event="Request",
            method=method,
            path=url,
        )

        log.msg(**msg)

    def log_response(self, response) -> None:
        log = self.log.bind(event_id=str(uuid.uuid4()))

        # Генерируем cURL команду
        curl = Curlify(response.request).to_curl()
        print(curl)

        # Allure attachment для cURL
        allure.attach(
            curl,
            name="cURL Command",
            attachment_type=allure.attachment_type.TEXT
        )

        response_content = self._get_json(response)

        # Собираем данные ответа в словарь
        response_info = {
            "event": "response",
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }

        if isinstance(response_content, (dict, list)):
            response_info["json_response"] = response_content
        else:
            response_info["content"] = response_content

        # Форматированный JSON для вывода и Allure
        formatted_response = json.dumps(response_info, indent=2, ensure_ascii=False)
        print(formatted_response)

        # Allure attachment для ответа (только JSON данные)
        if isinstance(response_content, (dict, list)):
            allure.attach(
                json.dumps(response_content, indent=2, ensure_ascii=False),
                name=f"Response JSON: {response.status_code}",
                attachment_type=allure.attachment_type.JSON
            )

        log.msg(
            event="Response",
            status_code=response.status_code,
        )

    @staticmethod
    def _get_json(response) -> dict[str, Any] | list | bytes:
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.content


class RequestHandler:
    def __init__(self, auth_token: Optional[str] = None):
        self.auth_token = auth_token
        self.session = requests.Session()
        self._configure_retries()
        self.logger = Logging()

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
            data: Optional[Union[bytes, str]] = None,
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

        # ИСПРАВЛЕНИЕ: передаем правильные данные в log_request
        self.logger.log_request(
            request.method,
            request.url,
            data=data,
            headers=headers,
            params=params,
            json=payload
        )

        return request.prepare()

    def send_request(
            self, prepared_request: requests.PreparedRequest, path: str
    ) -> requests.Response:
        response = self.session.send(prepared_request)
        self.logger.log_response(response)

        return response

    def validate_response(
            self,
            response: requests.Response,
            expected_status: Optional[HTTPStatus],
            method: str,
            payload: Optional[Dict] = None,
    ):
        if response.status_code != expected_status.value:
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
        logger.info(f"{response.status_code} | {method} | {formatted_path}")

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