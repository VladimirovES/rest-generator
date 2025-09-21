from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient
from .models import (
    CheckRoleGroupNameNotExistRequest,
    CreateRoleGroupRequest,
    GetRoleGroupFilterRequest,
    PaginatedResponseBase,
    RoleGroupFilterType,
    RoleGroupResponse,
    SetUsersForRoleGroupRequest,
    UpdateRoleGroupRequest,
)


class RoleGroups:

    def __init__(self, client: ApiClient):
        self._client = client

    def create_role_group(
        self,
        project_oid: str,
        payload: CreateRoleGroupRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> RoleGroupResponse:
        """
        Создать ролевую группу
        """
        with allure.step(
            "Create Role Group (POST /projects/{project_oid}/role-groups)"
        ):
            path = f"/projects/{project_oid}/role-groups"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            RoleGroupResponse(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def get_my_role_group(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Получить мою ролевую группу
        """
        with allure.step(
            "Get My Role Group (GET /projects/{project_oid}/role-groups/me)"
        ):
            path = f"/projects/{project_oid}/role-groups/me"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def check_role_group_name(
        self,
        project_oid: str,
        payload: CheckRoleGroupNameNotExistRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Проверить, что название группы не занята
        """
        with allure.step(
            "Check Role Group Name (POST /projects/{project_oid}/role-groups/check-name)"
        ):
            path = f"/projects/{project_oid}/role-groups/check-name"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def search_role_groups(
        self,
        project_oid: str,
        payload: GetRoleGroupFilterRequest,
        limit: Optional[Any] = None,
        offset: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseRoleGroupResponse:
        """
        Получить ролевые группы
        """
        with allure.step(
            "Search Role Groups (POST /projects/{project_oid}/role-groups/search)"
        ):
            path = f"/projects/{project_oid}/role-groups/search"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "limit": limit,
                    "offset": offset,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PaginatedResponseRoleGroupResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_filters_values(
        self,
        project_oid: str,
        limit: Optional[Any] = None,
        offset: Optional[Any] = None,
        search: Optional[Any] = None,
        filter_type: Optional[RoleGroupFilterType] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseBase:
        """
        Получить значения для фильтрации
        """
        with allure.step(
            "Get Filters Values (GET /projects/{project_oid}/role-groups/filters)"
        ):
            path = f"/projects/{project_oid}/role-groups/filters"

            r_json = self._client.get(
                path=path,
                params={
                    "limit": limit,
                    "offset": offset,
                    "search": search,
                    "filter_type": filter_type,
                    **(params or {}),
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PaginatedResponseBase(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def update_role_group(
        self,
        role_group_id: str,
        project_oid: str,
        payload: UpdateRoleGroupRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> RoleGroupResponse:
        """
        Обновить ролевую группу
        """
        with allure.step(
            "Update Role Group (PUT /projects/{project_oid}/role-groups/{role_group_id})"
        ):
            path = f"/projects/{project_oid}/role-groups/{role_group_id}"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            RoleGroupResponse(**r_json) if expected_status == HTTPStatus.OK else r_json
        )

    def set_users_for_role_group(
        self,
        role_group_id: str,
        project_oid: str,
        payload: SetUsersForRoleGroupRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Редактировать список пользователей
        """
        with allure.step(
            "Set Users For Role Group (PUT /projects/{project_oid}/role-groups/{role_group_id}/users)"
        ):
            path = f"/projects/{project_oid}/role-groups/{role_group_id}/users"

            r_json = self._client.put(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json
