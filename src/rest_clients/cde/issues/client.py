from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient
from .models import (
    ChangeStatusIssueRequestSchema,
    CreateIssueCommentRequestSchema,
    CreateIssueRequestSchema,
    CreateIssueResponseSchema,
    IssueCommentResponseSchema,
    IssueFilterSchema,
    IssueForAdminFilterSchema,
    IssuePaginationResponseSchema,
    IssueProcessNumberOfCurrent,
    IssueResponseSchema,
    ListIssueResponseSchema,
)


class Issues:

    def __init__(self, client: ApiClient):
        self._client = client

    def get_number_of_current(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> IssueProcessNumberOfCurrent:
        """
        Метод позволяет получить количество замечаний, где пользователь является автором или ответственным с определенным статусом
        """
        with allure.step(
            "Get Number Of Current (GET /projects/{project_oid}/issues/number_of_current)"
        ):
            path = f"/projects/{project_oid}/issues/number_of_current"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            IssueProcessNumberOfCurrent(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_issue(
        self,
        issue_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> IssueResponseSchema:
        """
        Получение замечания
        """
        with allure.step("Get Issue (GET /projects/{project_oid}/issues/{issue_oid})"):
            path = f"/projects/{project_oid}/issues/{issue_oid}"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            IssueResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def list_issues(
        self,
        entity_oid: str,
        project_oid: str,
        payload: IssueFilterSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ListIssueResponseSchema:
        """
        Получение замечаний
        """
        with allure.step(
            "List Issues (POST /projects/{project_oid}/entity/{entity_oid}/issues)"
        ):
            path = f"/projects/{project_oid}/entity/{entity_oid}/issues"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ListIssueResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def change_status_issue(
        self,
        issue_oid: str,
        project_oid: str,
        payload: ChangeStatusIssueRequestSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> IssueResponseSchema:
        """
        Обновление статуса замечания
        """
        with allure.step(
            "Change Status Issue (PUT /projects/{project_oid}/issues/{issue_oid}/status)"
        ):
            path = f"/projects/{project_oid}/issues/{issue_oid}/status"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            IssueResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def create_issue(
        self,
        entity_version_oid: str,
        project_oid: str,
        payload: CreateIssueRequestSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateIssueResponseSchema:
        """
        Создание замечания
        """
        with allure.step(
            "Create Issue (POST /projects/{project_oid}/entity_version/{entity_version_oid}/issues/add)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/issues/add"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CreateIssueResponseSchema(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def create_issues_comment(
        self,
        issue_oid: str,
        project_oid: str,
        payload: CreateIssueCommentRequestSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> IssueCommentResponseSchema:
        """
        Добавление комментария к замечанию
        """
        with allure.step(
            "Create Issues Comment (POST /projects/{project_oid}/issues/{issue_oid}/comment)"
        ):
            path = f"/projects/{project_oid}/issues/{issue_oid}/comment"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            IssueCommentResponseSchema(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def list_issues_for_admin(
        self,
        payload: IssueForAdminFilterSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> IssuePaginationResponseSchema:
        """
        Получение реестра замечаний
        """
        with allure.step("List Issues For Admin (POST /issues)"):
            path = f"/issues"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            IssuePaginationResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
