from http import HTTPStatus
import allure

from typing import Any, Optional, Dict
from rest_client.client import ApiClient
from .models import ModelLayerFilesResponse, ModelLayerRequest, PagePaginatorResponse


class ModelLayers:

    def __init__(self, client: ApiClient):
        self._client = client

    def get_model_layers(
        self,
        project_oid: str,
        entity_version_oid: str,
        checklist_oid: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ModelLayerFilesResponse:
        """
        Запрос на получение списка Слоев в модели
        """
        with allure.step(
            "Get Model Layers (GET /projects/{project_oid}/entity_versions/{entity_version_oid}/model_layers/)"
        ):
            path = f"/projects/{project_oid}/entity_versions/{entity_version_oid}/model_layers/"

            r_json = self._client.get(
                path=path,
                params={"checklist_oid": checklist_oid, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ModelLayerFilesResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_model_layers(
        self,
        project_oid: str,
        entity_version_oid: str,
        payload: ModelLayerRequest,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> PagePaginatorResponse:
        """
        Запрос на получение списка Слоев в модели
        """
        with allure.step(
            "Get Model Layers (POST /projects/{project_oid}/entity_versions/{entity_version_oid}/model_layers/search)"
        ):
            path = f"/projects/{project_oid}/entity_versions/{entity_version_oid}/model_layers/search"

            r_json = self._client.post(
                path=path,
                payload=payload,
                params={
                    "page": page,
                    "page_size": page_size,
                },
                headers=headers,
                expected_status=expected_status,
            )
        return (
            PagePaginatorResponse(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
