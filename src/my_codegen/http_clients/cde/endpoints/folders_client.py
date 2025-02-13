from http import HTTPStatus
from typing import Any, Optional, List, Dict
from my_codegen.http_clients.api_client import ApiClient
from http_clients.cde.models import (
    BlockFolderRequest,
    CheckBlockFolderResponse,
    CreateFolderRequest,
    FolderResponse,
    MoveFolderRequest,
    PatchFolderRequest,
    RetrieveFolderResponse,
)

import allure


class Folders(ApiClient):
    _service = "/cde"

    @allure.step("Блокировка папок")
    def block_folders(
        self,
        project_oid: str,
        payload: List[BlockFolderRequest],
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> Any:

        path = f"/projects/{project_oid}/folders/block"
        r_json = self._post(
            path=self._service + path,
            payload=[item.dict() for item in payload],
            expected_status=status,
        )

        return r_json

    @allure.step("Проверка блокировки папок")
    def check_block_folders(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[CheckBlockFolderResponse]:

        path = f"/projects/{project_oid}/folders/block"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            [CheckBlockFolderResponse(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Разблокировка папок")
    def unblock_folders(
        self,
        project_oid: str,
        payload: List[BlockFolderRequest],
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:

        path = f"/projects/{project_oid}/folders/block"
        r_json = self._delete(
            path=self._service + path,
            payload=[item.dict() for item in payload],
            expected_status=status,
        )

        return r_json

    @allure.step("Получение корневых папок")
    def get_folders(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[FolderResponse]:

        path = f"/projects/{project_oid}/folders"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            [FolderResponse(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Создание папок")
    def create_folders(
        self,
        project_oid: str,
        payload: List[CreateFolderRequest],
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[FolderResponse]:

        path = f"/projects/{project_oid}/folders"
        r_json = self._post(
            path=self._service + path,
            payload=[item.dict() for item in payload],
            expected_status=status,
        )

        return (
            [FolderResponse(**item) for item in r_json]
            if status == HTTPStatus.CREATED
            else r_json
        )

    @allure.step("Получение папки и ее дочерней структуры")
    def get_folder_by_oid(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> RetrieveFolderResponse:

        path = f"/projects/{project_oid}/folders/{folder_oid}"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return RetrieveFolderResponse(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Изменение папки")
    def patch_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: PatchFolderRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> FolderResponse:

        path = f"/projects/{project_oid}/folders/{folder_oid}"
        r_json = self._patch(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return FolderResponse(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Удаление папки")
    def delete_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:

        path = f"/projects/{project_oid}/folders/{folder_oid}"
        r_json = self._delete(path=self._service + path, expected_status=status)

        return r_json

    @allure.step("Перемещение папки")
    def move_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: MoveFolderRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> FolderResponse:

        path = f"/projects/{project_oid}/folders/{folder_oid}/move"
        r_json = self._patch(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return FolderResponse(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Скачать папку и ее содержимое")
    def queue_folder_for_download(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/folders/{folder_oid}/download"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return r_json

    @allure.step("Восстановление папки из архива")
    def restore_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/folders/{folder_oid}/restore"
        r_json = self._post(path=self._service + path, expected_status=status)

        return r_json
