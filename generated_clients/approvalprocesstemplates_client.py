from http import HTTPStatus
from typing import Any, Optional, Dict
from api_client import ApiClientServices
from models import (
    ApprovalProcessTemplateFilterReqeust,
    ApprovalProcessTemplateFullResponseSchema,
    CreateApprovalProcessTemplateRequest,
    CreateApprovalProcessTemplateResponseSchema,
    PaginatedApprovalProcessTemplateResponse,
)


class ApprovalProcessTemplates(ApiClientServices):
    def create_approval_process_template(
        self,
        project_oid: str,
        payload: CreateApprovalProcessTemplateRequest,
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateApprovalProcessTemplateResponseSchema:
        """
        Создание нового шаблона процесса согласования
        """
        path = f"/projects/{project_oid}/approval_process_templates"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateApprovalProcessTemplateResponseSchema(**r_json)
            if status == HTTPStatus.CREATED
            else r_json
        )

    def get_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalProcessTemplateFullResponseSchema:
        """
        Получение информации о конкретном шаблоне согласования
        """
        path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            ApprovalProcessTemplateFullResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    def update_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        payload: CreateApprovalProcessTemplateRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> CreateApprovalProcessTemplateResponseSchema:
        """
        Редактирование существующего шаблона согласования
        """
        path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"
        r_json = self.put(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateApprovalProcessTemplateResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    def delete_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление шаблона процесса согласования
        """
        path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"
        r_json = self.delete(path=path, expected_status=status)

        return r_json

    def search_approval_process_templates(
        self,
        project_oid: str,
        payload: ApprovalProcessTemplateFilterReqeust,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedApprovalProcessTemplateResponse:
        """
        Поиск шаблонов процессов согласования с фильтрацией и пагинацией
        """
        path = f"/projects/{project_oid}/approval_process_templates/search"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PaginatedApprovalProcessTemplateResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
