from http import HTTPStatus
import allure

from typing import Any, Optional, List, Dict
from my_codegen.rest_client.client import ApiClient
from .models import StatusPutRequest, StatusUpdate


class PassStatus:

    def __init__(self, client: ApiClient):
        self._client = client

    def route_get_handler(
        self,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[ApiHandlersStatusDtoStatusRead]:
        """ """
        with allure.step("Route Get Handler (GET /pass_status)"):
            path = f"/pass_status"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [ApiHandlersStatusDtoStatusRead(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def route_put_data_handler(
        self,
        access_pass_oid: str,
        project_oid: str,
        payload: StatusUpdate,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> StatusPutRequest:
        """ """
        with allure.step(
            "Route Put Data Handler (PUT /projects/{project_oid}/access_passes/{access_pass_oid}/status)"
        ):
            path = f"/projects/{project_oid}/access_passes/{access_pass_oid}/status"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            StatusPutRequest(**r_json) if expected_status == HTTPStatus.OK else r_json
        )
