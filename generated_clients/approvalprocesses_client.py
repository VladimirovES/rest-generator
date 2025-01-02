from http import HTTPStatus
from typing import Any, Optional, Dict
from api_client import ApiClientServices
from models import (
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


class ApprovalProcesses(ApiClientServices):
    def create_approval_process(
        self,
        project_oid: str,
        payload: CreateApprovalProcessRequest,
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateApprovalProcessResponseSchema:
        """
        Создание нового процесса согласования
        """
        path = f"/projects/{project_oid}/approval_processes"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateApprovalProcessResponseSchema(**r_json)
            if status == HTTPStatus.CREATED
            else r_json
        )

    def check_objects_for_approval_process(
        self,
        project_oid: str,
        payload: CheckObjectsForApprovalProcessRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Проверка сущностей и папок на предмет возможности создания согласования
        """
        path = f"/projects/{project_oid}/approval_processes/check"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    def search_approval_processes(
        self,
        project_oid: str,
        payload: SearchApprovalProcessesRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PagePaginatorResponseApprovalProcessResponseShortSchema:
        """
        Получение списка процессов согласования с фильтрацией и пагинацией
        """
        path = f"/projects/{project_oid}/approval_processes/search"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PagePaginatorResponseApprovalProcessResponseShortSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    def get_approval_process_detail(
        self,
        approval_process_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalProcessFullResponseSchema:
        """
        Получение подробной информации о процессе согласования
        """
        path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            ApprovalProcessFullResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    def get_approval_process_step(
        self,
        step_oid: str,
        approval_process_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalStepFullResponseSchema:
        """
        Получение информации о конкретном шаге согласования
        """
        path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}/steps/{step_oid}"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            ApprovalStepFullResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    def approve_step(
        self,
        step_oid: str,
        approval_process_oid: str,
        project_oid: str,
        payload: ActionRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Согласование или отклонение шага процесса
        """
        path = f"/projects/{project_oid}/approval_processes/{approval_process_oid}/steps/{step_oid}/action"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    def get_approval_processes_log(
        self,
        project_oid: str,
        payload: SearchApprovalProcessesLogsRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PagePaginatorResponseApprovalProcessLogResponseSchema:
        """
        Получение журнала действий по процессам согласования
        """
        path = f"/projects/{project_oid}/approval_processes/log"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PagePaginatorResponseApprovalProcessLogResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
