import json
from typing import Any

try:
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False
    allure = None

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False
    structlog = None

try:
    from curlify2 import Curlify
    CURLIFY_AVAILABLE = True
except ImportError:
    CURLIFY_AVAILABLE = False
    Curlify = None


class Logging:
    def __init__(self) -> None:
        if STRUCTLOG_AVAILABLE:
            self.log = structlog.get_logger(__name__).bind(service="api")
        else:
            self.log = None

    def _extract_json_data(self, json_data: Any, content: Any, data: Any) -> Any:
        if json_data:
            return json_data
        try:
            if content:
                return json.loads(content)
            elif data and isinstance(data, str):
                return json.loads(data)
        except json.JSONDecodeError:
            pass
        return None

    def log_request(self, method: str, url: str, **kwargs: Any) -> None:
        json_data = self._extract_json_data(
            kwargs.get("json"),
            kwargs.get("content"),
            kwargs.get("data")
        )

        request_info = {
            "event": "request",
            "method": method,
            "url": url
        }

        for key in ["params", "headers"]:
            if kwargs.get(key):
                request_info[key] = kwargs[key]

        if json_data:
            request_info["payload"] = json_data
        elif kwargs.get("data"):
            request_info["data"] = kwargs["data"]

        print(json.dumps(request_info, indent=2, ensure_ascii=False))

        if json_data and ALLURE_AVAILABLE:
            allure.attach(
                json.dumps(json_data, indent=2, ensure_ascii=False),
                name=f"Request: {method} {url}",
                attachment_type=allure.attachment_type.JSON
            )

    def log_curl(self, response) -> None:
        if CURLIFY_AVAILABLE:
            curl = Curlify(response.request).to_curl()
            print(curl)

            if ALLURE_AVAILABLE:
                allure.attach(
                    curl,
                    name="cURL Command",
                    attachment_type=allure.attachment_type.TEXT
                )
        else:
            print(f"cURL: {response.request.method} {response.request.url}")

    def log_response(self, response) -> None:
        response_content = self._get_json(response)

        response_info = {
            "event": "response",
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }

        if isinstance(response_content, (dict, list)):
            response_info["json_response"] = response_content
        else:
            response_info["content"] = response_content

        print(json.dumps(response_info, indent=2, ensure_ascii=False))

        if isinstance(response_content, (dict, list)) and ALLURE_AVAILABLE:
            allure.attach(
                json.dumps(response_content, indent=2, ensure_ascii=False),
                name=f"Response JSON: {response.status_code}",
                attachment_type=allure.attachment_type.JSON
            )

    @staticmethod
    def _get_json(response) -> dict[str, Any] | list | bytes:
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.content