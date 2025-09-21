from http import HTTPStatus
import allure

from typing import Optional, Dict
from rest_client.client import ApiClient
from .models import ModelSystemChecklistRequest, ModelSystemChecklistResponse


class ModelSystems:

    def __init__(self, client: ApiClient):
        self._client = client

    def get_model_system_checklist(
        self,
        project_oid: str,
        system_oid: str,
        payload: ModelSystemChecklistRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ModelSystemChecklistResponse:
        """
        Запрос на получение списка категорий и количества пунктов в них по чек-листу системы
        """
        with allure.step(
            "Get Model System Checklist (POST /projects/{project_oid}/model_systems/{system_oid}/checklist)"
        ):
            path = f"/projects/{project_oid}/model_systems/{system_oid}/checklist"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ModelSystemChecklistResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
