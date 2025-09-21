from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from my_codegen.rest_client.client import ApiClient
from .models import InspectorResult, LivenessResult


class Probe:

    def __init__(self, client: ApiClient):
        self._client = client

    def route_get_handler(
        self,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> LivenessResult:
        """ """
        with allure.step("Route Get Handler (GET /liveness)"):
            path = f"/liveness"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return LivenessResult(**r_json) if expected_status == HTTPStatus.OK else r_json

    def route_get_handler(
        self,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> InspectorResult:
        """ """
        with allure.step("Route Get Handler (GET /readiness)"):
            path = f"/readiness"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return InspectorResult(**r_json) if expected_status == HTTPStatus.OK else r_json

    def route_get_handler(
        self,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> InspectorResult:
        """ """
        with allure.step("Route Get Handler (GET /health)"):
            path = f"/health"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return InspectorResult(**r_json) if expected_status == HTTPStatus.OK else r_json
