from http import HTTPStatus
import allure

from typing import Any, Optional, List, Dict
from rest_client.client import ApiClient
from .models import AccessSettingResponse, UpdateAccessSettingRequestSchema


class AccessSetting:

    def __init__(self, client: ApiClient):
        self._client = client

    def get_access_setting_for_folder(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> AccessSettingResponse:
        """
        Получить настройки доступа на папку
        """
        with allure.step(
            "Get Access Setting For Folder (GET /projects/{project_oid}/folders/{folder_oid}/access-setting)"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}/access-setting"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            AccessSettingResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def update_access_setting_for_folder(
        self,
        project_oid: str,
        folder_oid: str,
        payload: UpdateAccessSettingRequestSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Настройка доступа на папку
        """
        with allure.step(
            "Update Access Setting For Folder (PUT /projects/{project_oid}/folders/{folder_oid}/access-setting)"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}/access-setting"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def get_access_setting_for_entity(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> AccessSettingResponse:
        """
        Получить настройки доступа на файл
        """
        with allure.step(
            "Get Access Setting For Entity (GET /projects/{project_oid}/entity/{entity_oid}/access-setting)"
        ):
            path = f"/projects/{project_oid}/entity/{entity_oid}/access-setting"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            AccessSettingResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def update_access_setting_for_entity(
        self,
        project_oid: str,
        entity_oid: str,
        payload: UpdateAccessSettingRequestSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Настройка доступа на файл
        """
        with allure.step(
            "Update Access Setting For Entity (PUT /projects/{project_oid}/entity/{entity_oid}/access-setting)"
        ):
            path = f"/projects/{project_oid}/entity/{entity_oid}/access-setting"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def get_access_permissions_for_entity(
        self,
        project_oid: str,
        entity_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[str]:
        """
        Получить доступные разрешения на файл
        """
        with allure.step(
            "Get Access Permissions For Entity (GET /projects/{project_oid}/entity/{entity_oid}/access)"
        ):
            path = f"/projects/{project_oid}/entity/{entity_oid}/access"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return [item for item in r_json] if expected_status == HTTPStatus.OK else r_json

    def get_access_permissions_for_folder(
        self,
        project_oid: str,
        folder_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[str]:
        """
        Получить доступные разрешения на папку
        """
        with allure.step(
            "Get Access Permissions For Folder (GET /projects/{project_oid}/folders/{folder_oid}/access)"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}/access"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return [item for item in r_json] if expected_status == HTTPStatus.OK else r_json

    def get_users_with_access_for_entity(
        self,
        entity_oid: str,
        project_oid: str,
        role_group: str,
        limit: Optional[Any] = None,
        offset: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithPermissionResponse:
        """
        Получить пользователей с доступами на файл
        """
        with allure.step(
            "Get Users With Access For Entity (GET /projects/{project_oid}/entity/{entity_oid}/access/users)"
        ):
            path = f"/projects/{project_oid}/entity/{entity_oid}/access/users"

            r_json = self._client.get(
                path=path,
                params={
                    "limit": limit,
                    "offset": offset,
                    "role_group": role_group,
                    **(params or {}),
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PaginatedResponseUserWithPermissionResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_users_with_access_for_folder(
        self,
        folder_oid: str,
        project_oid: str,
        role_group: str,
        limit: Optional[Any] = None,
        offset: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithPermissionResponse:
        """
        Получить пользователей с доступами на папку
        """
        with allure.step(
            "Get Users With Access For Folder (GET /projects/{project_oid}/folders/{folder_oid}/access/users)"
        ):
            path = f"/projects/{project_oid}/folders/{folder_oid}/access/users"

            r_json = self._client.get(
                path=path,
                params={
                    "limit": limit,
                    "offset": offset,
                    "role_group": role_group,
                    **(params or {}),
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PaginatedResponseUserWithPermissionResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
