from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient
from .models import (
    ApprovalProcessTemplateFilterReqeust,
    ApprovalProcessTemplateFullResponseSchema,
    CreateApprovalProcessTemplateRequest,
    CreateApprovalProcessTemplateResponseSchema,
    PaginatedApprovalProcessTemplateResponse,
)


class ApprovalProcessTemplates:

    def __init__(self, client: ApiClient):
        self._client = client

    def create_approval_process_template(
        self,
        project_oid: str,
        payload: CreateApprovalProcessTemplateRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateApprovalProcessTemplateResponseSchema:
        """
        Создание нового шаблона процесса согласования
        """
        with allure.step(
            "Create Approval Process Template (POST /projects/{project_oid}/approval_process_templates)"
        ):
            path = f"/projects/{project_oid}/approval_process_templates"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CreateApprovalProcessTemplateResponseSchema(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def get_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalProcessTemplateFullResponseSchema:
        """
        Получение информации о конкретном шаблоне согласования
        """
        with allure.step(
            "Get Approval Process Template (GET /projects/{project_oid}/approval_process_templates/{template_oid})"
        ):
            path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ApprovalProcessTemplateFullResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def update_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        payload: CreateApprovalProcessTemplateRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> CreateApprovalProcessTemplateResponseSchema:
        """
        Редактирование существующего шаблона согласования
        """
        with allure.step(
            "Update Approval Process Template (PUT /projects/{project_oid}/approval_process_templates/{template_oid})"
        ):
            path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CreateApprovalProcessTemplateResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def delete_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление шаблона процесса согласования
        """
        with allure.step(
            "Delete Approval Process Template (DELETE /projects/{project_oid}/approval_process_templates/{template_oid})"
        ):
            path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"

            r_json = self._client.delete(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def search_approval_process_templates(
        self,
        project_oid: str,
        payload: ApprovalProcessTemplateFilterReqeust,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedApprovalProcessTemplateResponse:
        """
        Поиск шаблонов процессов согласования с фильтрацией и пагинацией
        """
        with allure.step(
            "Search Approval Process Templates (POST /projects/{project_oid}/approval_process_templates/search)"
        ):
            path = f"/projects/{project_oid}/approval_process_templates/search"

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
            PaginatedApprovalProcessTemplateResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
