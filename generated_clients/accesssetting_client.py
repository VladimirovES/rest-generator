from http import HTTPStatus
from typing import Any, Optional, List, Dict
from api_client import ApiClientServices
from models import (
    AccessSettingResponse,
    PaginatedResponseUserWithPermissionResponse,
    UpdateAccessSettingRequestSchema,
)


class AccessSetting(ApiClientServices):
    def update_access_setting_for_folder(
        self,
        project_oid: str,
        folder_oid: str,
        payload: UpdateAccessSettingRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Настройка доступа на папку
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}/access-setting"
        r_json = self.put(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    def get_access_setting_for_folder(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> AccessSettingResponse:
        """
        Получить настройки доступа на папку
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}/access-setting"
        r_json = self.get(path=path, params=params, expected_status=status)

        return AccessSettingResponse(**r_json) if status == HTTPStatus.OK else r_json

    def update_access_setting_for_entity(
        self,
        project_oid: str,
        entity_oid: str,
        payload: UpdateAccessSettingRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Настройка доступа на файл
        """
        path = f"/projects/{project_oid}/entity/{entity_oid}/access-setting"
        r_json = self.put(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    def get_access_setting_for_entity(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> AccessSettingResponse:
        """
        Получить настройки доступа на файл
        """
        path = f"/projects/{project_oid}/entity/{entity_oid}/access-setting"
        r_json = self.get(path=path, params=params, expected_status=status)

        return AccessSettingResponse(**r_json) if status == HTTPStatus.OK else r_json

    def get_access_permissions_for_entity(
        self,
        project_oid: str,
        entity_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[str]:
        """
        Получить доступные разрешения на файл
        """
        path = f"/projects/{project_oid}/entity/{entity_oid}/access"
        r_json = self.get(path=path, params=params, expected_status=status)

        return [str(**item) for item in r_json] if status == HTTPStatus.OK else r_json

    def get_access_permissions_for_folder(
        self,
        project_oid: str,
        folder_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[str]:
        """
        Получить доступные разрешения на папку
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}/access"
        r_json = self.get(path=path, params=params, expected_status=status)

        return [str(**item) for item in r_json] if status == HTTPStatus.OK else r_json

    def get_users_with_access_for_entity(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithPermissionResponse:
        """
        Получить пользователей с доступами на файл
        """
        path = f"/projects/{project_oid}/entity/{entity_oid}/access/users"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            PaginatedResponseUserWithPermissionResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    def get_users_with_access_for_folder(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithPermissionResponse:
        """
        Получить пользователей с доступами на папку
        """
        path = f"/projects/{project_oid}/folders/{folder_oid}/access/users"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            PaginatedResponseUserWithPermissionResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
