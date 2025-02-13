from http import HTTPStatus
from typing import Any, Optional, Dict
from my_codegen.http_clients.api_client import ApiClient
from http_clients.cde.models import (
    ChangeStatusIssueRequestSchema,
    CreateIssueRequestSchema,
    CreateIssueResponseSchema,
    IssueFilterSchema,
    IssueForAdminFilterSchema,
    IssuePaginationResponseSchema,
    IssueResponseSchema,
    ListIssueResponseSchema,
)

import allure


class Issues(ApiClient):
    _service = "/cde"

    @allure.step("Получение замечания")
    def get_issue(
        self,
        issue_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> IssueResponseSchema:

        path = f"/projects/{project_oid}/issues/{issue_oid}"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return IssueResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Получение замечаний")
    def list_issues(
        self,
        entity_oid: str,
        project_oid: str,
        payload: IssueFilterSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ListIssueResponseSchema:

        path = f"/projects/{project_oid}/entity/{entity_oid}/issues"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return ListIssueResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Обновление статуса замечания")
    def change_status_issue(
        self,
        issue_oid: str,
        project_oid: str,
        payload: ChangeStatusIssueRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> IssueResponseSchema:

        path = f"/projects/{project_oid}/issues/{issue_oid}/status"
        r_json = self._put(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return IssueResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Создание замечания")
    def create_issue(
        self,
        entity_version_oid: str,
        project_oid: str,
        payload: CreateIssueRequestSchema,
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateIssueResponseSchema:

        path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/issues/add"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateIssueResponseSchema(**r_json)
            if status == HTTPStatus.CREATED
            else r_json
        )

    @allure.step("Получение замечаний(для администратора)")
    def list_issues_for_admin(
        self, payload: IssueForAdminFilterSchema, status: HTTPStatus = HTTPStatus.OK
    ) -> IssuePaginationResponseSchema:

        path = f"/issues"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            IssuePaginationResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
