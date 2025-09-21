from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient
from .models import GetUsersFilterRequest


class Users:

    def __init__(self, client: ApiClient):
        self._client = client

    def get_users(
        self,
        project_oid: str,
        payload: GetUsersFilterRequest,
        limit: Optional[Any] = None,
        offset: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithRoleGroupResponse:
        """
        Получить пользователей с проекта
        """
        with allure.step("Get Users (POST /projects/{project_oid}/users)"):
            path = f"/projects/{project_oid}/users"

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
            PaginatedResponseUserWithRoleGroupResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
