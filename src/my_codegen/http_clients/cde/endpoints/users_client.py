from http import HTTPStatus
from my_codegen.http_clients.api_client import ApiClient
from http_clients.cde.models import (
    GetUsersFilterRequest,
    PaginatedResponseUserWithRoleGroupResponse,
)

import allure


class Users(ApiClient):
    _service = "/cde"

    @allure.step("Получить пользователей с проекта")
    def get_users(
        self,
        project_oid: str,
        payload: GetUsersFilterRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithRoleGroupResponse:

        path = f"/projects/{project_oid}/users"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PaginatedResponseUserWithRoleGroupResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
