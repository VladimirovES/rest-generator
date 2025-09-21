from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient


class Permissions:

    def __init__(self, client: ApiClient):
        self._client = client

    def get_permissions(
        self,
        limit: Optional[Any] = None,
        offset: Optional[Any] = None,
        permission__in: Optional[Any] = None,
        code_name__not_in: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseRolePermissionResponse:
        """
        Получение разрешений для ролевой
        """
        with allure.step("Get Permissions (GET /permissions)"):
            path = f"/permissions"

            r_json = self._client.get(
                path=path,
                params={
                    "limit": limit,
                    "offset": offset,
                    "permission__in": permission__in,
                    "code_name__not_in": code_name__not_in,
                    **(params or {}),
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PaginatedResponseRolePermissionResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
