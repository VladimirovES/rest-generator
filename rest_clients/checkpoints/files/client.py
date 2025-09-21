from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from my_codegen.rest_client.client import ApiClient
from .models import FileResponse


class Files:

    def __init__(self, client: ApiClient):
        self._client = client

    def route_create(
        self,
        payload: BodyRouteCreateFilesPost,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> FileResponse:
        """ """
        with allure.step("Route Create (POST /files)"):
            path = f"/files"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            FileResponse(**r_json) if expected_status == HTTPStatus.CREATED else r_json
        )

    def route_delete_handler(
        self,
        file_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """ """
        with allure.step("Route Delete Handler (DELETE /files/{file_oid})"):
            path = f"/files/{file_oid}"

            r_json = self._client.delete(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json
