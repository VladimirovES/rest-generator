from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from my_codegen.rest_client.client import ApiClient
from .models import (
    SearchBodyFilters,
    SearchBodyGetFilters,
    VisitSessionGet,
    VisitSessionPut,
    VisitSessionRead,
)


class VisitSessions:

    def __init__(self, client: ApiClient):
        self._client = client

    def route_post_handler(
        self,
        access_pass_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> VisitSessionRead:
        """ """
        with allure.step(
            "Route Post Handler (POST /projects/{project_oid}/access_passes/{access_pass_oid}/visit_sessions)"
        ):
            path = f"/projects/{project_oid}/access_passes/{access_pass_oid}/visit_sessions"

            r_json = self._client.post(
                path=path, headers=headers, expected_status=expected_status
            )
        return (
            VisitSessionRead(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def route_get_handler(
        self,
        visit_session_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> VisitSessionGet:
        """ """
        with allure.step(
            "Route Get Handler (GET /projects/{project_oid}/visit_sessions/{visit_session_oid})"
        ):
            path = f"/projects/{project_oid}/visit_sessions/{visit_session_oid}"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return VisitSessionGet(**r_json) if expected_status == HTTPStatus.OK else r_json

    def route_put_handler(
        self,
        visit_session_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> VisitSessionPut:
        """ """
        with allure.step(
            "Route Put Handler (PUT /projects/{project_oid}/visit_sessions/{visit_session_oid})"
        ):
            path = f"/projects/{project_oid}/visit_sessions/{visit_session_oid}"

            r_json = self._client.put(
                path=path, headers=headers, expected_status=expected_status
            )
        return VisitSessionPut(**r_json) if expected_status == HTTPStatus.OK else r_json

    def route_post_data_handler(
        self,
        project_oid: str,
        payload: SearchBodyGetFilters,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> ObjectsPageAuthorRead:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /projects/{project_oid}/controllers)"
        ):
            path = f"/projects/{project_oid}/controllers"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ObjectsPageAuthorRead(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def route_post_data_handler(
        self,
        project_oid: str,
        payload: SearchBodyFilters,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> ObjectsPageVisitSessionSearchResponse:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /projects/{project_oid}/visit_sessions/search)"
        ):
            path = f"/projects/{project_oid}/visit_sessions/search"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ObjectsPageVisitSessionSearchResponse(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )
