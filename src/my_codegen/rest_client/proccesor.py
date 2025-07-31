import json
from typing import Union, Dict, List, Optional, Any
from http import HTTPStatus

import requests
from requests.adapters import HTTPAdapter, Retry
from pydantic import BaseModel, RootModel

from .logging_client import Logging


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
        if payload is None:
            return None

        if isinstance(payload, BaseModel):
            return payload.model_dump_json()

        if isinstance(payload, list) and payload and isinstance(payload[0], BaseModel):
            ListModel = RootModel[List[type(payload[0])]]
            return ListModel(payload).model_dump_json()

        if isinstance(payload, (dict, list)):
            return json.dumps(payload, ensure_ascii=False)

        return str(payload)

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

        self.logger.log_curl(response)
        self.logger.log_response(response)

        return response

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