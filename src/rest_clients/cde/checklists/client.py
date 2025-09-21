from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient
from .models import (
    CheckListCreateRequest,
    CheckListDownloadRequest,
    CheckListFreeResponseSchema,
    CheckListItemCreateRequest,
    CheckListItemResponseSchema,
    CheckListItemUpdateRequest,
    CheckListItemsUpdateRequest,
    CheckListResponseSchema,
    CheckListRetrieveRequest,
    CheckListRetrieveResponseSchema,
    CheckListUpdateRequest,
    CheckTitleRequest,
    CheckTitleResponse,
    CreatedCheckListItemsResponseSchema,
    PagePaginatorResponse,
    SearchCheckListRequest,
    UpdatedCheckListItemsResponseSchema,
)


class Checklists:

    def __init__(self, client: ApiClient):
        self._client = client

    def create_checklist(
        self,
        project_oid: str,
        payload: CheckListCreateRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CheckListResponseSchema:
        """
        Метод используется для создания чек-листа по Помещению, Системе или Свободному чек-листа
        """
        with allure.step(
            "Create Checklist (POST /projects/{project_oid}/checklists/create)"
        ):
            path = f"/projects/{project_oid}/checklists/create"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CheckListResponseSchema(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def search_checklist(
        self,
        project_oid: str,
        payload: SearchCheckListRequest,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PagePaginatorResponse:
        """
        Метод используется для получения списка доступных пользователю чек-листов
        """
        with allure.step(
            "Search Checklist (POST /projects/{project_oid}/checklists/search)"
        ):
            path = f"/projects/{project_oid}/checklists/search"

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
            PagePaginatorResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_checklist(
        self,
        checklist_oid: str,
        project_oid: str,
        payload: CheckListRetrieveRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> CheckListRetrieveResponseSchema:
        """
        Метод используется для получения данных по доступному для пользователя чек-листу - пункты чек-листа
        """
        with allure.step(
            "Get Checklist (POST /projects/{project_oid}/checklists/{checklist_oid})"
        ):
            path = f"/projects/{project_oid}/checklists/{checklist_oid}"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CheckListRetrieveResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def update_checklist(
        self,
        checklist_oid: str,
        project_oid: str,
        payload: CheckListUpdateRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> CheckListResponseSchema:
        """
        Метод используется для редактирования существующего чек-листа
        """
        with allure.step(
            "Update Checklist (PATCH /projects/{project_oid}/checklists/{checklist_oid})"
        ):
            path = f"/projects/{project_oid}/checklists/{checklist_oid}"

            r_json = self._client.patch(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CheckListResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def delete_checklist(
        self,
        checklist_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Метод используется для удаления (soft-delete) чек-листа
        """
        with allure.step(
            "Delete Checklist (DELETE /projects/{project_oid}/checklists/{checklist_oid})"
        ):
            path = f"/projects/{project_oid}/checklists/{checklist_oid}"

            r_json = self._client.delete(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def download_checklist(
        self,
        checklist_oid: str,
        project_oid: str,
        payload: CheckListDownloadRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Метод используется для скачивания определенного чек-листа в определенном формате
        """
        with allure.step(
            "Download Checklist (POST /projects/{project_oid}/checklists/{checklist_oid}/download)"
        ):
            path = f"/projects/{project_oid}/checklists/{checklist_oid}/download"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def update_checklist_item(
        self,
        checklist_oid: str,
        item_oid: str,
        project_oid: str,
        payload: CheckListItemUpdateRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> CheckListItemResponseSchema:
        """
        Метод используется для редактирования пункта чек-листа
        """
        with allure.step(
            "Update Checklist Item (PATCH /projects/{project_oid}/checklists/{checklist_oid}/checklist_items/{item_oid})"
        ):
            path = f"/projects/{project_oid}/checklists/{checklist_oid}/checklist_items/{item_oid}"

            r_json = self._client.patch(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CheckListItemResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def create_checklist_items(
        self,
        checklist_oid: str,
        project_oid: str,
        payload: CheckListItemCreateRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreatedCheckListItemsResponseSchema:
        """
        Метод используется для создания категории/пункта Свободного чек-листа
        """
        with allure.step(
            "Create Checklist Items (POST /projects/{project_oid}/checklists/{checklist_oid}/checklist_items)"
        ):
            path = f"/projects/{project_oid}/checklists/{checklist_oid}/checklist_items"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CreatedCheckListItemsResponseSchema(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def update_checklist_items(
        self,
        checklist_oid: str,
        project_oid: str,
        payload: CheckListItemsUpdateRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> UpdatedCheckListItemsResponseSchema:
        """
        Метод для обновления значений параметров пункта чек-листа при заполнении/оценке пункта чеклиста
        """
        with allure.step(
            "Update Checklist Items (PUT /projects/{project_oid}/checklists/{checklist_oid}/checklist_items)"
        ):
            path = f"/projects/{project_oid}/checklists/{checklist_oid}/checklist_items"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            UpdatedCheckListItemsResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def check_unique_category_title_in_checklist_items(
        self,
        project_oid: str,
        checklist_oid: str,
        payload: CheckTitleRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> CheckTitleResponse:
        """
        Проверки уникальности названия категории пункта чек-листа
        """
        with allure.step(
            "Check Unique Category Title In Checklist Items (POST /projects/{project_oid}/checklists/{checklist_oid}/check-category-title)"
        ):
            path = f"/projects/{project_oid}/checklists/{checklist_oid}/check-category-title"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CheckTitleResponse(**r_json) if expected_status == HTTPStatus.OK else r_json
        )

    def get_free_checklist(
        self,
        checklist_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> CheckListFreeResponseSchema:
        """
        Метод используется для получения данных по доступному для пользователя чек-листу - с группировкой по категориям
        """
        with allure.step(
            "Get Free Checklist (POST /projects/{project_oid}/free-checklists/{checklist_oid})"
        ):
            path = f"/projects/{project_oid}/free-checklists/{checklist_oid}"

            r_json = self._client.post(
                path=path, headers=headers, expected_status=expected_status
            )
        return (
            CheckListFreeResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
