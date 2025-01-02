from http import HTTPStatus
from typing import Any, Optional, Dict
from api_client import ApiClientServices
from models import (
    CheckRoleGroupNameNotExistRequest,
    CreateRoleGroupRequest,
    GetRoleGroupFilterRequest,
    PaginatedResponseBase,
    PaginatedResponseRoleGroupResponse,
    RoleGroupResponse,
    SetUsersForRoleGroupRequest,
    UpdateRoleGroupRequest,
)


class RoleGroups(ApiClientServices):
    def create_role_group(
        self,
        project_oid: str,
        payload: CreateRoleGroupRequest,
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> RoleGroupResponse:
        """
        Создать ролевую группу
        """
        path = f"/projects/{project_oid}/role-groups"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return RoleGroupResponse(**r_json) if status == HTTPStatus.CREATED else r_json

    def get_my_role_group(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Получить мою ролевую группу
        """
        path = f"/projects/{project_oid}/role-groups/me"
        r_json = self.get(path=path, params=params, expected_status=status)

        return r_json

    def check_role_group_name(
        self,
        project_oid: str,
        payload: CheckRoleGroupNameNotExistRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Проверить, что название группы не занята
        """
        path = f"/projects/{project_oid}/role-groups/check-name"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    def search_role_groups(
        self,
        project_oid: str,
        payload: GetRoleGroupFilterRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseRoleGroupResponse:
        """
        Получить ролевые группы
        """
        path = f"/projects/{project_oid}/role-groups/search"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PaginatedResponseRoleGroupResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    def get_filters_values(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseBase:
        """
        Получить значения для фильтрации
        """
        path = f"/projects/{project_oid}/role-groups/filters"
        r_json = self.get(path=path, params=params, expected_status=status)

        return PaginatedResponseBase(**r_json) if status == HTTPStatus.OK else r_json

    def update_role_group(
        self,
        role_group_id: str,
        project_oid: str,
        payload: UpdateRoleGroupRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> RoleGroupResponse:
        """
        Обновить ролевую группу
        """
        path = f"/projects/{project_oid}/role-groups/{role_group_id}"
        r_json = self.put(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return RoleGroupResponse(**r_json) if status == HTTPStatus.OK else r_json

    def set_users_for_role_group(
        self,
        role_group_id: str,
        project_oid: str,
        payload: SetUsersForRoleGroupRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Редактировать список пользователей
        """
        path = f"/projects/{project_oid}/role-groups/{role_group_id}/users"
        r_json = self.put(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json
