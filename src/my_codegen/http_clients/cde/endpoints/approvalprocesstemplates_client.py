from http import HTTPStatus
from typing import Any, Optional, Dict
from my_codegen.http_clients.api_client import ApiClient
from http_clients.cde.models import (
    ApprovalProcessTemplateFilterReqeust,
    ApprovalProcessTemplateFullResponseSchema,
    CreateApprovalProcessTemplateRequest,
    CreateApprovalProcessTemplateResponseSchema,
    PaginatedApprovalProcessTemplateResponse,
)

import allure


class ApprovalProcessTemplates(ApiClient):
    _service = "/cde"

    @allure.step("Создание нового шаблона процесса согласования")
    def create_approval_process_template(
        self,
        project_oid: str,
        payload: CreateApprovalProcessTemplateRequest,
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateApprovalProcessTemplateResponseSchema:

        path = f"/projects/{project_oid}/approval_process_templates"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateApprovalProcessTemplateResponseSchema(**r_json)
            if status == HTTPStatus.CREATED
            else r_json
        )

    @allure.step("Получение информации о конкретном шаблоне согласования")
    def get_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ApprovalProcessTemplateFullResponseSchema:

        path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            ApprovalProcessTemplateFullResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Редактирование существующего шаблона согласования")
    def update_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        payload: CreateApprovalProcessTemplateRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> CreateApprovalProcessTemplateResponseSchema:

        path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"
        r_json = self._put(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateApprovalProcessTemplateResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Удаление шаблона процесса согласования")
    def delete_approval_process_template(
        self,
        template_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:

        path = f"/projects/{project_oid}/approval_process_templates/{template_oid}"
        r_json = self._delete(path=self._service + path, expected_status=status)

        return r_json

    @allure.step("Поиск шаблонов процессов согласования с фильтрацией и пагинацией")
    def search_approval_process_templates(
        self,
        project_oid: str,
        payload: ApprovalProcessTemplateFilterReqeust,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedApprovalProcessTemplateResponse:

        path = f"/projects/{project_oid}/approval_process_templates/search"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PaginatedApprovalProcessTemplateResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
