from http import HTTPStatus
import allure

from typing import Any, Optional, List, Dict
from my_codegen.rest_client.client import ApiClient
from .models import ReportFilterResponse, ReportPage, ReportSearchData


class Report:

    def __init__(self, client: ApiClient):
        self._client = client

    def route_get_handler(
        self,
        domain: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[ReportFilterResponse]:
        """ """
        with allure.step(
            "Route Get Handler (GET /reportings/access_pass/project/{project_oid}/filter-fields)"
        ):
            path = f"/reportings/access_pass/project/{project_oid}/filter-fields"

            r_json = self._client.get(
                path=path,
                params={"domain": domain, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [ReportFilterResponse(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def route_retrieve_handler(
        self,
        project_oid: str,
        field: str,
        search: str,
        domain: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """ """
        with allure.step(
            "Route Retrieve Handler (GET /reportings/access_pass/project/{project_oid}/filters)"
        ):
            path = f"/reportings/access_pass/project/{project_oid}/filters"

            r_json = self._client.get(
                path=path,
                params={
                    "field": field,
                    "search": search,
                    "domain": domain,
                    **(params or {}),
                },
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def route_post_data_handler(
        self,
        project_oid: str,
        page: int,
        per_page: int,
        domain: str,
        payload: ReportSearchData,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> ReportPage:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /reportings/access_pass/project/{project_oid})"
        ):
            path = f"/reportings/access_pass/project/{project_oid}"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "page": page,
                    "per_page": per_page,
                    "domain": domain,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return ReportPage(**r_json) if expected_status == HTTPStatus.CREATED else r_json

    def route_get_handler(
        self,
        domain: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[ReportFilterResponse]:
        """ """
        with allure.step(
            "Route Get Handler (GET /reportings/visit_session/project/{project_oid}/filter-fields)"
        ):
            path = f"/reportings/visit_session/project/{project_oid}/filter-fields"

            r_json = self._client.get(
                path=path,
                params={"domain": domain, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [ReportFilterResponse(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def route_retrieve_handler(
        self,
        project_oid: str,
        field: str,
        search: str,
        domain: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """ """
        with allure.step(
            "Route Retrieve Handler (GET /reportings/visit_session/project/{project_oid}/filters)"
        ):
            path = f"/reportings/visit_session/project/{project_oid}/filters"

            r_json = self._client.get(
                path=path,
                params={
                    "field": field,
                    "search": search,
                    "domain": domain,
                    **(params or {}),
                },
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def route_post_data_handler(
        self,
        project_oid: str,
        page: int,
        per_page: int,
        domain: str,
        payload: ReportSearchData,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> ReportPage:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /reportings/visit_session/project/{project_oid})"
        ):
            path = f"/reportings/visit_session/project/{project_oid}"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "page": page,
                    "per_page": per_page,
                    "domain": domain,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return ReportPage(**r_json) if expected_status == HTTPStatus.CREATED else r_json
