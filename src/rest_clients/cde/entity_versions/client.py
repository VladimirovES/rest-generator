from http import HTTPStatus
import allure

from typing import Any, Optional, List, Dict
from rest_client.client import ApiClient
from .models import (
    Categories,
    CheckTitleRequest,
    CheckTitleResponse,
    EntityVersionS3PathResponseSchema,
    ModelElementShortResponseSchema,
    ModelRoomResponse,
    PropertyModelSchema,
    RoomPassportResponseSchema,
    SystemPassportResponseSchema,
    TileResponseSchema,
)


class EntityVersions:

    def __init__(self, client: ApiClient):
        self._client = client

    def get_model_rooms(
        self,
        entity_version_oid: str,
        project_oid: str,
        name: Optional[Any] = None,
        number: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[ModelRoomResponse]:
        """
        Получение списка помещений по модели
        """
        with allure.step(
            "Get Model Rooms (GET /projects/{project_oid}/entity_version/{entity_version_oid}/model_rooms)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/model_rooms"

            r_json = self._client.get(
                path=path,
                params={"name": name, "number": number, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [ModelRoomResponse(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_model_systems(
        self,
        entity_version_oid: str,
        project_oid: str,
        system_name: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[Categories]:
        """
        Получение списка систем по модели
        """
        with allure.step(
            "Get Model Systems (GET /projects/{project_oid}/entity_version/{entity_version_oid}/model_systems)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/model_systems"

            r_json = self._client.get(
                path=path,
                params={"system_name": system_name, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [Categories(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def check_unique_title_in_checklists(
        self,
        project_oid: str,
        entity_version_oid: str,
        payload: CheckTitleRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> CheckTitleResponse:
        """
        Проверки уникальности названия чек-листа
        """
        with allure.step(
            "Check Unique Title In Checklists (POST /projects/{project_oid}/entity_version/{entity_version_oid}/checklists/check-checklist-title)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/checklists/check-checklist-title"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CheckTitleResponse(**r_json) if expected_status == HTTPStatus.OK else r_json
        )

    def get_entity_version_path_s3(
        self,
        entity_version_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityVersionS3PathResponseSchema:
        """ """
        with allure.step(
            "Get Entity Version Path S3 (GET /projects/{project_oid}/entity_version/{entity_version_oid}/path_s3)"
        ):
            path = (
                f"/projects/{project_oid}/entity_version/{entity_version_oid}/path_s3"
            )

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            EntityVersionS3PathResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_properties(
        self,
        entity_version_oid: str,
        project_oid: str,
        room_oid: Optional[Any] = None,
        system_oid: Optional[Any] = None,
        element_ifc: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PropertyModelSchema:
        """
        Запрос свойств Помещения/Системы/Элемента
        """
        with allure.step(
            "Get Properties (GET /projects/{project_oid}/entity_version/{entity_version_oid}/properties)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/properties"

            r_json = self._client.get(
                path=path,
                params={
                    "room_oid": room_oid,
                    "system_oid": system_oid,
                    "element_ifc": element_ifc,
                    **(params or {}),
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PropertyModelSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_room_passport(
        self,
        entity_version_oid: str,
        project_oid: str,
        room_oid: Optional[Any] = None,
        ifc_id: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> RoomPassportResponseSchema:
        """
        Frontend направляет запрос на получение паспорта помещения
        """
        with allure.step(
            "Get Room Passport (GET /projects/{project_oid}/entity_version/{entity_version_oid}/room_passport)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/room_passport"

            r_json = self._client.get(
                path=path,
                params={"room_oid": room_oid, "ifc_id": ifc_id, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            RoomPassportResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_system_passport(
        self,
        entity_version_oid: str,
        project_oid: str,
        system_oid: Optional[Any] = None,
        ifc_id: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> SystemPassportResponseSchema:
        """
        Frontend направляет запрос на получение паспорта системы
        """
        with allure.step(
            "Get System Passport (GET /projects/{project_oid}/entity_version/{entity_version_oid}/system_passport)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/system_passport"

            r_json = self._client.get(
                path=path,
                params={"system_oid": system_oid, "ifc_id": ifc_id, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            SystemPassportResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_model_elements(
        self,
        entity_version_oid: str,
        project_oid: str,
        system_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[ModelElementShortResponseSchema]:
        """
        Получить элементы по версии
        """
        with allure.step(
            "Get Model Elements (GET /projects/{project_oid}/entity_version/{entity_version_oid}/model_elements)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/model_elements"

            r_json = self._client.get(
                path=path,
                params={"system_oid": system_oid, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [ModelElementShortResponseSchema(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_tiles(
        self,
        entity_version_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> TileResponseSchema:
        """
        Плитки для вьювера
        """
        with allure.step(
            "Get Tiles (GET /projects/{project_oid}/entity_version/{entity_version_oid}/tiles)"
        ):
            path = f"/projects/{project_oid}/entity_version/{entity_version_oid}/tiles"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            TileResponseSchema(**r_json) if expected_status == HTTPStatus.OK else r_json
        )
