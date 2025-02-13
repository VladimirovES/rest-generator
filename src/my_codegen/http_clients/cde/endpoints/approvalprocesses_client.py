from http import HTTPStatus
from typing import Any, Optional, Dict
from my_codegen.http_clients.api_client import ApiClient
from http_clients.cde.models import (
    ActionRequest,
    ApprovalProcessFullResponseSchema,
    ApprovalStepFullResponseSchema,
    CheckObjectsForApprovalProcessRequest,
    CreateApprovalProcessRequest,
    CreateApprovalProcessResponseSchema,
    PagePaginatorResponseApprovalProcessLogResponseSchema,
    PagePaginatorResponseApprovalProcessResponseShortSchema,
    SearchApprovalProcessesLogsRequest,
    SearchApprovalProcessesRequest,
)

import allure


class ApprovalProcesses(ApiClient):
    _service = "/cde"

    @allure.step("Создание нового процесса согласования")
    def create_approval_process(
        self,
        project_oid: str,
        payload: CreateApprovalProcessRequest,
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateApprovalProcessResponseSchema:

        path = f"/projects/{project_oid}/approval_processes"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateApprovalProcessResponseSchema(**r_json)
            if status == HTTPStatus.CREATED
            else r_json
        )

    @allure.step(
        "Проверка сущностей и папок на предмет возможности создания согласования"
    )
    def check_objects_for_approval_process(
        self,
        project_oid: str,
        payload: CheckObjectsForApprovalProcessRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/approval_processes/check"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    @allure.step("Получение списка процессов согласования с фильтрацией и пагинацией")
    def search_approval_processes(
        self,
        project_oid: str,
        payload: SearchApprovalProcessesRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PagePaginatorResponseApprovalProcessResponseShortSchema:

        path = f"/projects/{project_oid}/approval_processes/search"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PagePaginatorResponseApprovalProcessResponseShortSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Получение подробной информации о процессе согласования")
    def get_approval_process_detail(
        self,
        approval_process_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalProcessFullResponseSchema:

        path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            ApprovalProcessFullResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Получение информации о конкретном шаге согласования")
    def get_approval_process_step(
        self,
        step_oid: str,
        approval_process_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalStepFullResponseSchema:

        path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}/steps/{step_oid}"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            ApprovalStepFullResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Согласование или отклонение шага процесса")
    def approve_step(
        self,
        step_oid: str,
        approval_process_oid: str,
        project_oid: str,
        payload: ActionRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}/steps/{step_oid}/action"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    @allure.step("Получение журнала действий по процессам согласования")
    def get_approval_processes_log(
        self,
        project_oid: str,
        payload: SearchApprovalProcessesLogsRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PagePaginatorResponseApprovalProcessLogResponseSchema:

        path = f"/projects/{project_oid}/approval_processes/log"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PagePaginatorResponseApprovalProcessLogResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
