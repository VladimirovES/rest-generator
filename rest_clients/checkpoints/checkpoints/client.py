from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from my_codegen.rest_client.client import ApiClient
from .models import CheckpointCreate, CheckpointSearchData, CheckpointUpdate


class Checkpoints:

    def __init__(self, client: ApiClient):
        self._client = client

    def route_post_data_handler(
        self,
        project_oid: str,
        payload: CheckpointCreate,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CheckpointCreate:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /projects/{project_oid}/checkpoints)"
        ):
            path = f"/projects/{project_oid}/checkpoints"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CheckpointCreate(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def route_put_data_handler(
        self,
        checkpoint_oid: str,
        project_oid: str,
        payload: CheckpointUpdate,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> CheckpointUpdate:
        """ """
        with allure.step(
            "Route Put Data Handler (PUT /projects/{project_oid}/checkpoints/{checkpoint_oid})"
        ):
            path = f"/projects/{project_oid}/checkpoints/{checkpoint_oid}"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CheckpointUpdate(**r_json) if expected_status == HTTPStatus.OK else r_json
        )

    def route_delete_handler(
        self,
        checkpoint_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """ """
        with allure.step(
            "Route Delete Handler (DELETE /projects/{project_oid}/checkpoints/{checkpoint_oid})"
        ):
            path = f"/projects/{project_oid}/checkpoints/{checkpoint_oid}"

            r_json = self._client.delete(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def route_post_data_handler(
        self,
        project_oid: str,
        payload: CheckpointSearchData,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ObjectsPageCheckpointRead:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /projects/{project_oid}/checkpoints/search)"
        ):
            path = f"/projects/{project_oid}/checkpoints/search"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ObjectsPageCheckpointRead(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
