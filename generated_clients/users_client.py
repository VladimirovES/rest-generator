from http import HTTPStatus
from api_client import ApiClientServices
from models import GetUsersFilterRequest, PaginatedResponseUserWithRoleGroupResponse


class Users(ApiClientServices):
    def get_users(
        self,
        project_oid: str,
        payload: GetUsersFilterRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> PaginatedResponseUserWithRoleGroupResponse:
        """
        Получить пользователей с проекта
        """
        path = f"/projects/{project_oid}/users"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            PaginatedResponseUserWithRoleGroupResponse(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )
