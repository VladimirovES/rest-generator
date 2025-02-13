from http import HTTPStatus
from typing import Any, Optional, List, Dict
from my_codegen.http_clients.api_client import ApiClient
from http_clients.cde.models import (
    BlockEntityResponseSchema,
    BodyRemoveFilesFromStorageProjectsProjectOidEntitiesFilesRemoveFromStoragePost,
    CheckContentRequestSchema,
    ContentCheckResponseSchema,
    CreateEntityRequestSchema,
    CreateEntityVersionResponseSchema,
    EntityFullResponseSchema,
    EntityResponseSchema,
    EntityVersionFullResponseSchema,
    EntityVersionListResponseSchema,
    EntityVersionRequestSchema,
    FileResponseSchema,
    GenerateFileUploadLinkRequestSchema,
    MoveEntityRequest,
    PatchEntityRequestSchema,
)

import allure


class Entities(ApiClient):
    _service = "/cde"

    @allure.step("Получение списка сущностей")
    def list_entities(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[EntityResponseSchema]:

        path = f"/projects/{project_oid}/entities"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            [EntityResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Создание сущностей")
    def create_entities(
        self,
        project_oid: str,
        payload: List[CreateEntityRequestSchema],
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[EntityResponseSchema]:

        path = f"/projects/{project_oid}/entities"
        r_json = self._post(
            path=self._service + path,
            payload=[item.dict() for item in payload],
            expected_status=status,
        )

        return (
            [EntityResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.CREATED
            else r_json
        )

    @allure.step("Получение сущности по oid")
    def get_entity(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityFullResponseSchema:

        path = f"/projects/{project_oid}/entities/{entity_oid}"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return EntityFullResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Изменение сущности")
    def patch_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: PatchEntityRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityResponseSchema:

        path = f"/projects/{project_oid}/entities/{entity_oid}"
        r_json = self._patch(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return EntityResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Удаление сущности")
    def delete_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:

        path = f"/projects/{project_oid}/entities/{entity_oid}"
        r_json = self._delete(path=self._service + path, expected_status=status)

        return r_json

    @allure.step("Получение ссылок для загрузки файлов")
    def generate_upload_urls(
        self,
        project_oid: str,
        payload: List[GenerateFileUploadLinkRequestSchema],
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[FileResponseSchema]:

        path = f"/projects/{project_oid}/entities/generate-upload-urls"
        r_json = self._post(
            path=self._service + path,
            payload=[item.dict() for item in payload],
            expected_status=status,
        )

        return (
            [FileResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.CREATED
            else r_json
        )

    @allure.step("Перемещение сущности")
    def move_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: MoveEntityRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityResponseSchema:

        path = f"/projects/{project_oid}/entities/{entity_oid}/move"
        r_json = self._patch(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return EntityResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    @allure.step("Восстановление сущности из архива")
    def restore_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/entities/{entity_oid}/restore"
        r_json = self._post(path=self._service + path, expected_status=status)

        return r_json

    @allure.step("Проверка, что файл не занят другим пользователем")
    def get_entity_block(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> BlockEntityResponseSchema:

        path = f"/projects/{project_oid}/entities/{entity_oid}/check"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            BlockEntityResponseSchema(**r_json) if status == HTTPStatus.OK else r_json
        )

    @allure.step("Блокировка файла")
    def block_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> BlockEntityResponseSchema:

        path = f"/projects/{project_oid}/entities/{entity_oid}/block"
        r_json = self._post(path=self._service + path, expected_status=status)

        return (
            BlockEntityResponseSchema(**r_json) if status == HTTPStatus.OK else r_json
        )

    @allure.step("Продление блокировки файла")
    def continue_block_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:

        path = f"/projects/{project_oid}/entities/{entity_oid}/block/continue"
        r_json = self._post(path=self._service + path, expected_status=status)

        return r_json

    @allure.step("Разблокировка файла")
    def unblock_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/entities/{entity_oid}/unblock"
        r_json = self._post(path=self._service + path, expected_status=status)

        return r_json

    @allure.step(
        "Получение ссылки на скачивание файлов определенной версии сущности из хранилища"
    )
    def get_entity_files_download_url(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[FileResponseSchema]:

        path = f"/projects/{project_oid}/entities/{entity_oid}/download"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            [FileResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Получение списка версий сущности")
    def get_entity_versions(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[EntityVersionListResponseSchema]:

        path = f"/projects/{project_oid}/entities/{entity_oid}/versions"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            [EntityVersionListResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Создание новой версии сущности (прикрепление файлов новой версии)")
    def create_entity_new_version(
        self,
        entity_oid: str,
        project_oid: str,
        payload: EntityVersionRequestSchema,
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateEntityVersionResponseSchema:

        path = f"/projects/{project_oid}/entities/{entity_oid}/versions"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateEntityVersionResponseSchema(**r_json)
            if status == HTTPStatus.CREATED
            else r_json
        )

    @allure.step("Получение версии сущности по oid")
    def get_entity_version(
        self,
        version_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityVersionFullResponseSchema:

        path = f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}"
        r_json = self._get(
            path=self._service + path, params=params, expected_status=status
        )

        return (
            EntityVersionFullResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    @allure.step("Удаление версии сущности")
    def delete_entity_version(
        self,
        entity_oid: str,
        version_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:

        path = f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}"
        r_json = self._delete(path=self._service + path, expected_status=status)

        return r_json

    @allure.step("Восстановление версии сущности из архива")
    def restore_entity_version(
        self,
        version_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:

        path = f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}/restore"
        r_json = self._post(path=self._service + path, expected_status=status)

        return r_json

    @allure.step("Удалить файлы из хранилища")
    def remove_files_from_storage(
        self,
        project_oid: str,
        payload: BodyRemoveFilesFromStorageProjectsProjectOidEntitiesFilesRemoveFromStoragePost,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:

        path = f"/projects/{project_oid}/entities/files/remove-from-storage"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    @allure.step("Проверка файла/модели")
    def check_content(
        self,
        entity_oid: str,
        project_oid: str,
        payload: CheckContentRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ContentCheckResponseSchema:

        path = f"/projects/{project_oid}/entities/{entity_oid}/check-content"
        r_json = self._post(
            path=self._service + path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            ContentCheckResponseSchema(**r_json) if status == HTTPStatus.OK else r_json
        )
