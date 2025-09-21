from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from my_codegen.rest_client.client import ApiClient
from .models import (
    AccessPassCreate,
    AccessPassPDFData,
    AccessPassPDFResponse,
    AccessPassRead,
    AccessPassSearchData,
    AccessPassShortRead,
    AuthorSearchData,
)


class AccessPasses:

    def __init__(self, client: ApiClient):
        self._client = client

    def route_post_data_handler(
        self,
        project_oid: str,
        payload: AccessPassCreate,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> AccessPassShortRead:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /projects/{project_oid}/access_passes)"
        ):
            path = f"/projects/{project_oid}/access_passes"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            AccessPassShortRead(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def route_retrieve_handler(
        self,
        access_pass_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> AccessPassRead:
        """ """
        with allure.step(
            "Route Retrieve Handler (GET /projects/{project_oid}/access_passes/{access_pass_oid})"
        ):
            path = f"/projects/{project_oid}/access_passes/{access_pass_oid}"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return AccessPassRead(**r_json) if expected_status == HTTPStatus.OK else r_json

    def route_put_data_handler(
        self,
        access_pass_oid: str,
        project_oid: str,
        payload: AccessPassCreate,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> AccessPassShortRead:
        """ """
        with allure.step(
            "Route Put Data Handler (PUT /projects/{project_oid}/access_passes/{access_pass_oid})"
        ):
            path = f"/projects/{project_oid}/access_passes/{access_pass_oid}"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            AccessPassShortRead(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def route_post_data_handler(
        self,
        project_oid: str,
        payload: AccessPassSearchData,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ObjectsPageAccessPassSearch:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /projects/{project_oid}/access_passes/search)"
        ):
            path = f"/projects/{project_oid}/access_passes/search"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ObjectsPageAccessPassSearch(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def route_put_data_handler(
        self,
        access_pass_oid: str,
        project_oid: str,
        payload: AccessPassPDFData,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> AccessPassPDFResponse:
        """ """
        with allure.step(
            "Route Put Data Handler (PUT /projects/{project_oid}/access_passes/{access_pass_oid}/agreed_document)"
        ):
            path = f"/projects/{project_oid}/access_passes/{access_pass_oid}/agreed_document"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            AccessPassPDFResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def route_post_data_handler(
        self,
        project_oid: str,
        payload: AuthorSearchData,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> ObjectsPageAuthorRead:
        """ """
        with allure.step(
            "Route Post Data Handler (POST /projects/{project_oid}/authors)"
        ):
            path = f"/projects/{project_oid}/authors"

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
