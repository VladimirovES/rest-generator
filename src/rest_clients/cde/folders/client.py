from http import HTTPStatus
import allure

from typing import Any, Optional, List, Dict
from rest_client.client import ApiClient
from .models import (
    BlockFolderRequest,
    CheckBlockFolderResponse,
    CreateFolderRequest,
    FolderResponse,
    MoveFolderRequest,
    PatchFolderRequest,
    RetrieveFolderResponse,
)


class Folders:

    def __init__(self, client: ApiClient):
        self._client = client

    def check_block_folders(
        self,
        project_oid: str,
        folder_oids: List[str],
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[CheckBlockFolderResponse]:
        """
        Проверка блокировки папок
        """
        with allure.step(
            "Check Block Folders (GET /projects/{project_oid}/folders/block)"
        ):
            path = f"/projects/{project_oid}/folders/block"

            r_json = self._client.get(
                path=path,
                params={"folder_oids": folder_oids, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [CheckBlockFolderResponse(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def block_folders(
        self,
        project_oid: str,
        payload: List[BlockFolderRequest],
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> Any:
        """
        Блокировка папок
        """
        with allure.step("Block Folders (POST /projects/{project_oid}/folders/block)"):
            path = f"/projects/{project_oid}/folders/block"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def unblock_folders(
        self,
        project_oid: str,
        payload: List[BlockFolderRequest],
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Разблокировка папок
        """
        with allure.step(
            "Unblock Folders (DELETE /projects/{project_oid}/folders/block)"
        ):
            path = f"/projects/{project_oid}/folders/block"

            r_json = self._client.delete(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def get_folders(
        self,
        project_oid: str,
        is_deleted: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[FolderResponse]:
        """
        Получение корневых папок
        """
        with allure.step("Get Folders (GET /projects/{project_oid}/folders)"):
            path = f"/projects/{project_oid}/folders"

            r_json = self._client.get(
                path=path,
                params={"is_deleted": is_deleted, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [FolderResponse(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def create_folders(
        self,
        project_oid: str,
        payload: List[CreateFolderRequest],
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[FolderResponse]:
        """
        Создание папок
        """
        with allure.step("Create Folders (POST /projects/{project_oid}/folders)"):
            path = f"/projects/{project_oid}/folders"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [FolderResponse(**item) for item in r_json]
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def get_folder_by_oid(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> RetrieveFolderResponse:
        """
        Получение папки и ее дочерней структуры
        """
        with allure.step(
            "Get Folder By Oid (GET /projects/{project_oid}/folders/{folder_oid})"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            RetrieveFolderResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def patch_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: PatchFolderRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> FolderResponse:
        """
        Изменение папки
        """
        with allure.step(
            "Patch Folder (PATCH /projects/{project_oid}/folders/{folder_oid})"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}"

            r_json = self._client.patch(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return FolderResponse(**r_json) if expected_status == HTTPStatus.OK else r_json

    def delete_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление папки
        """
        with allure.step(
            "Delete Folder (DELETE /projects/{project_oid}/folders/{folder_oid})"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}"

            r_json = self._client.delete(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def move_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: MoveFolderRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> FolderResponse:
        """
        Перемещение папки
        """
        with allure.step(
            "Move Folder (PATCH /projects/{project_oid}/folders/{folder_oid}/move)"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}/move"

            r_json = self._client.patch(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return FolderResponse(**r_json) if expected_status == HTTPStatus.OK else r_json

    def queue_folder_for_download(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Скачать папку и ее содержимое
        """
        with allure.step(
            "Queue Folder For Download (GET /projects/{project_oid}/folders/{folder_oid}/download)"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}/download"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def restore_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Восстановление папки из архива
        """
        with allure.step(
            "Restore Folder (POST /projects/{project_oid}/folders/{folder_oid}/restore)"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}/restore"

            r_json = self._client.post(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json
