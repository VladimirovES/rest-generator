from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient
from .models import (
    ActionRequest,
    ApprovalProcessChecklistResponseSchema,
    ApprovalProcessFullResponseSchema,
    ApprovalProcessNumberOfCurrent,
    ApprovalProcessesCountResponse,
    ApprovalStepFullResponseSchema,
    CheckObjectsForApprovalProcessRequest,
    CountApprovalProcessesRequest,
    CreateApprovalProcessChecklistRequest,
    CreateApprovalProcessRequest,
    CreateApprovalProcessResponseSchema,
    SearchApprovalProcessesLogsRequest,
    SearchApprovalProcessesRequest,
)


class ApprovalProcesses:

    def __init__(self, client: ApiClient):
        self._client = client

    def create_approval_process(
        self,
        project_oid: str,
        payload: CreateApprovalProcessRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateApprovalProcessResponseSchema:
        """
        Создание нового процесса согласования
        """
        with allure.step(
            "Create Approval Process (POST /projects/{project_oid}/approval_processes)"
        ):
            path = f"/projects/{project_oid}/approval_processes"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CreateApprovalProcessResponseSchema(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def check_objects_for_approval_process(
        self,
        project_oid: str,
        payload: CheckObjectsForApprovalProcessRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Проверка сущностей и папок на предмет возможности создания согласования
        """
        with allure.step(
            "Check Objects For Approval Process (POST /projects/{project_oid}/approval_processes/check)"
        ):
            path = f"/projects/{project_oid}/approval_processes/check"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def search_approval_processes(
        self,
        project_oid: str,
        payload: SearchApprovalProcessesRequest,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PagePaginatorResponseApprovalProcessResponseShortSchema:
        """
        Получение списка процессов согласования с фильтрацией и пагинацией
        """
        with allure.step(
            "Search Approval Processes (POST /projects/{project_oid}/approval_processes/search)"
        ):
            path = f"/projects/{project_oid}/approval_processes/search"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "page": page,
                    "page_size": page_size,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PagePaginatorResponseApprovalProcessResponseShortSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_number_of_current(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalProcessNumberOfCurrent:
        """
        Метод позволяет получить количество согласований, где в текущем шаге пользователь из запроса является согласующим
        """
        with allure.step(
            "Get Number Of Current (GET /projects/{project_oid}/approval_processes/number_of_current)"
        ):
            path = f"/projects/{project_oid}/approval_processes/number_of_current"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ApprovalProcessNumberOfCurrent(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_approval_process_detail(
        self,
        approval_process_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalProcessFullResponseSchema:
        """
        Получение подробной информации о процессе согласования
        """
        with allure.step(
            "Get Approval Process Detail (GET /projects/{project_oid}/approval_processes/{approval_process_oid})"
        ):
            path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ApprovalProcessFullResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_approval_process_step(
        self,
        step_oid: str,
        approval_process_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalStepFullResponseSchema:
        """
        Получение информации о конкретном шаге согласования
        """
        with allure.step(
            "Get Approval Process Step (GET /projects/{project_oid}/approval_processes/{approval_process_oid}/steps/{step_oid})"
        ):
            path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}/steps/{step_oid}"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ApprovalStepFullResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def approve_step(
        self,
        step_oid: str,
        approval_process_oid: str,
        project_oid: str,
        payload: ActionRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Согласование или отклонение шага процесса
        """
        with allure.step(
            "Approve Step (POST /projects/{project_oid}/approval_processes/{approval_process_oid}/steps/{step_oid}/action)"
        ):
            path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}/steps/{step_oid}/action"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def get_approval_processes_log(
        self,
        project_oid: str,
        payload: SearchApprovalProcessesLogsRequest,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PagePaginatorResponseApprovalProcessLogResponseSchema:
        """
        Получение журнала действий по процессам согласования
        """
        with allure.step(
            "Get Approval Processes Log (POST /projects/{project_oid}/approval_processes/log)"
        ):
            path = f"/projects/{project_oid}/approval_processes/log"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "page": page,
                    "page_size": page_size,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PagePaginatorResponseApprovalProcessLogResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def create_approval_process_checklist(
        self,
        project_oid: str,
        payload: CreateApprovalProcessChecklistRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> ApprovalProcessChecklistResponseSchema:
        """
        Создание процесса согласования чек-листа
        """
        with allure.step(
            "Create Approval Process Checklist (POST /projects/{project_oid}/approval_processes/checklist)"
        ):
            path = f"/projects/{project_oid}/approval_processes/checklist"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ApprovalProcessChecklistResponseSchema(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def count_approval_processes(
        self,
        project_oid: str,
        payload: CountApprovalProcessesRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalProcessesCountResponse:
        """
        Получение счетчика входящих активных согласований
        """
        with allure.step(
            "Count Approval Processes (POST /projects/{project_oid}/approval_processes/count)"
        ):
            path = f"/projects/{project_oid}/approval_processes/count"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ApprovalProcessesCountResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
