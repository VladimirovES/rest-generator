from http import HTTPStatus
from typing import Any, Optional, Dict
from api_client import ApiClientServices
from models import PaginatedResponseRolePermissionResponse


class Permissions(ApiClientServices):
    def get_permissions(
        self,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseRolePermissionResponse:
        """
        Получение разрешений для ролевой
        """
        path = f"/permissions"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            PaginatedResponseRolePermissionResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
