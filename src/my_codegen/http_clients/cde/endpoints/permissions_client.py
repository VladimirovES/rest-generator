from http import HTTPStatus
from typing import Any, Optional, Dict
from my_codegen.http_clients.api_client import ApiClient
from http_clients.cde.models import PaginatedResponseRolePermissionResponse

import allure


class Permissions(ApiClient):
    _service = "/cde"

    @allure.step("Получение разрешений для ролевой")
    def get_permissions(
        self,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseRolePermissionResponse:

        path = f"/permissions"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            PaginatedResponseRolePermissionResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
