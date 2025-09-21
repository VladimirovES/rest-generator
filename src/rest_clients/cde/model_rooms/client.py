from http import HTTPStatus
import allure

from typing import Optional, Dict
from rest_client.client import ApiClient
from .models import ModelRoomChecklistRequest, ModelRoomChecklistResponse


class ModelRooms:

    def __init__(self, client: ApiClient):
        self._client = client

    def get_model_room_checklist(
        self,
        project_oid: str,
        room_oid: str,
        payload: ModelRoomChecklistRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ModelRoomChecklistResponse:
        """
        Запрос на получение списка категорий и количества пунктов в них по чек-листу помещения
        """
        with allure.step(
            "Get Model Room Checklist (POST /projects/{project_oid}/model_rooms/{room_oid}/checklist)"
        ):
            path = f"/projects/{project_oid}/model_rooms/{room_oid}/checklist"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ModelRoomChecklistResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
