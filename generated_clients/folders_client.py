from http import HTTPStatus
from typing import Any, Optional, List, Dict
from api_client import ApiClientServices
from models import (
    BlockFolderRequest,
    CheckBlockFolderResponse,
    CreateFolderRequest,
    FolderResponse,
    MoveFolderRequest,
    PatchFolderRequest,
    RetrieveFolderResponse,
)


class Folders(ApiClientServices):
    def block_folders(
        self,
        project_oid: str,
        payload: List[BlockFolderRequest],
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> Any:
        """
        Блокировка папок
        """
        path = f"/projects/{project_oid}/folders/block"
        r_json = self.post(
            path=path, payload=[item.dict() for item in payload], expected_status=status
        )

        return r_json

    def check_block_folders(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[CheckBlockFolderResponse]:
        """
        Проверка блокировки папок
        """
        path = f"/projects/{project_oid}/folders/block"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            [CheckBlockFolderResponse(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    def unblock_folders(
        self,
        project_oid: str,
        payload: List[BlockFolderRequest],
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Разблокировка папок
        """
        path = f"/projects/{project_oid}/folders/block"
        r_json = self.delete(
            path=path, payload=[item.dict() for item in payload], expected_status=status
        )

        return r_json

    def get_folders(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[FolderResponse]:
        """
        Получение корневых папок
        """
        path = f"/projects/{project_oid}/folders"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            [FolderResponse(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    def create_folders(
        self,
        project_oid: str,
        payload: List[CreateFolderRequest],
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[FolderResponse]:
        """
        Создание папок
        """
        path = f"/projects/{project_oid}/folders"
        r_json = self.post(
            path=path, payload=[item.dict() for item in payload], expected_status=status
        )

        return (
            [FolderResponse(**item) for item in r_json]
            if status == HTTPStatus.CREATED
            else r_json
        )

    def get_folder_by_oid(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> RetrieveFolderResponse:
        """
        Получение папки и ее дочерней структуры
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}"
        r_json = self.get(path=path, params=params, expected_status=status)

        return RetrieveFolderResponse(**r_json) if status == HTTPStatus.OK else r_json

    def patch_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: PatchFolderRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> FolderResponse:
        """
        Изменение папки
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}"
        r_json = self.patch(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return FolderResponse(**r_json) if status == HTTPStatus.OK else r_json

    def delete_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление папки
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}"
        r_json = self.delete(path=path, expected_status=status)

        return r_json

    def move_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: MoveFolderRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> FolderResponse:
        """
        Перемещение папки
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}/move"
        r_json = self.patch(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return FolderResponse(**r_json) if status == HTTPStatus.OK else r_json

    def queue_folder_for_download(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Скачать папку и ее содержимое
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}/download"
        r_json = self.get(path=path, params=params, expected_status=status)

        return r_json

    def restore_folder(
        self,
        folder_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Восстановление папки из архива
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}/restore"
        r_json = self.post(path=path, expected_status=status)

        return r_json
