from http import HTTPStatus
import allure

from typing import Optional, Dict
from my_codegen.rest_client.client import ApiClient
from .models import ProjectCreate


class Project:

    def __init__(self, client: ApiClient):
        self._client = client

    def route_post_data_handler(
        self,
        payload: ProjectCreate,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> ProjectCreate:
        """ """
        with allure.step("Route Post Data Handler (POST /project)"):
            path = f"/project"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ProjectCreate(**r_json) if expected_status == HTTPStatus.CREATED else r_json
        )
