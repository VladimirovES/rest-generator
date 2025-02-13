from http import HTTPStatus
from typing import Any, Optional, List, Dict
from my_codegen.http_clients.api_client import ApiClient
from http_clients.cde.models import (
    AccessSettingResponse,
    PaginatedResponseUserWithPermissionResponse,
    UpdateAccessSettingRequestSchema,
)

import allure


class AccessSetting(ApiClient):
    _service = "/cde"

    @allure.step("Настройка доступа на папку")
    def update_access_setting_for_folder(
        self,
        project_oid: str,
        folder_oid: str,
        payload: UpdateAccessSettingRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/folders/{folder_oid}/access-setting"
        r_json = self._put(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    @allure.step("Получить настройки доступа на папку")
    def get_access_setting_for_folder(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> AccessSettingResponse:

        path = f"/projects/{project_oid}/folders/{folder_oid}/access-setting"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return AccessSettingResponse(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Настройка доступа на файл")
    def update_access_setting_for_entity(
        self,
        project_oid: str,
        entity_oid: str,
        payload: UpdateAccessSettingRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/entity/{entity_oid}/access-setting"
        r_json = self._put(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    @allure.step("Получить настройки доступа на файл")
    def get_access_setting_for_entity(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> AccessSettingResponse:

        path = f"/projects/{project_oid}/entity/{entity_oid}/access-setting"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return AccessSettingResponse(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Получить доступные разрешения на файл")
    def get_access_permissions_for_entity(
        self,
        project_oid: str,
        entity_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[str]:

        path = f"/projects/{project_oid}/entity/{entity_oid}/access"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return [str(**item) for item in r_json] if status == HTTPStatus.OK else r_json

    @allure.step("Получить доступные разрешения на папку")
    def get_access_permissions_for_folder(
        self,
        project_oid: str,
        folder_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[str]:

        path = f"/projects/{project_oid}/folders/{folder_oid}/access"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return [str(**item) for item in r_json] if status == HTTPStatus.OK else r_json

    @allure.step("Получить пользователей с доступами на файл")
    def get_users_with_access_for_entity(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithPermissionResponse:

        path = f"/projects/{project_oid}/entity/{entity_oid}/access/users"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            PaginatedResponseUserWithPermissionResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Получить пользователей с доступами на папку")
    def get_users_with_access_for_folder(
        self,
        folder_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithPermissionResponse:

        path = f"/projects/{project_oid}/folders/{folder_oid}/access/users"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            PaginatedResponseUserWithPermissionResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
