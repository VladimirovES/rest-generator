from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient
from .models import (
    CreateElementDocumentRequest,
    ElementDocumentResponse,
    UpdateElementDocumentRequest,
)


class ElementDocuments:

    def __init__(self, client: ApiClient):
        self._client = client

    def update_element_documents(
        self,
        project_oid: str,
        entity_version_oid: str,
        element_oid: str,
        oid: str,
        payload: UpdateElementDocumentRequest,
        is_revit: Optional[bool] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ElementDocumentResponse:
        """
        Обновление документа элемента
        """
        with allure.step(
            "Update Element Documents (PUT /projects/{project_oid}/entity_versions/{entity_version_oid}/elements/{element_oid}/documents/{oid})"
        ):
            path = f"/projects/{project_oid}/entity_versions/{entity_version_oid}/elements/{element_oid}/documents/{oid}"

            r_json = self._client.put(
                path=path,
                payload=payload,
                params={
                    "is_revit": is_revit,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ElementDocumentResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def delete_element_documents(
        self,
        entity_version_oid: str,
        element_oid: str,
        oid: str,
        project_oid: str,
        is_revit: Optional[bool] = None,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление документа элемента
        """
        with allure.step(
            "Delete Element Documents (DELETE /projects/{project_oid}/entity_versions/{entity_version_oid}/elements/{element_oid}/documents/{oid})"
        ):
            path = f"/projects/{project_oid}/entity_versions/{entity_version_oid}/elements/{element_oid}/documents/{oid}"

            r_json = self._client.delete(
                path=path,
                params={
                    "is_revit": is_revit,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def list_element_documents(
        self,
        project_oid: str,
        entity_version_oid: str,
        element_oid: str,
        is_revit: Optional[bool] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ElementDocumentResponse:
        """
        Получение списка документов элемента
        """
        with allure.step(
            "List Element Documents (GET /projects/{project_oid}/entity_versions/{entity_version_oid}/elements/{element_oid}/documents/)"
        ):
            path = f"/projects/{project_oid}/entity_versions/{entity_version_oid}/elements/{element_oid}/documents/"

            r_json = self._client.get(
                path=path,
                params={"is_revit": is_revit, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ElementDocumentResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def create_element_documents(
        self,
        project_oid: str,
        entity_version_oid: str,
        element_oid: str,
        payload: CreateElementDocumentRequest,
        is_revit: Optional[bool] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> ElementDocumentResponse:
        """
        Создание документа элемента
        """
        with allure.step(
            "Create Element Documents (POST /projects/{project_oid}/entity_versions/{entity_version_oid}/elements/{element_oid}/documents/)"
        ):
            path = f"/projects/{project_oid}/entity_versions/{entity_version_oid}/elements/{element_oid}/documents/"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "is_revit": is_revit,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ElementDocumentResponse(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )
