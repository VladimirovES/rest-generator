from http import HTTPStatus
import allure

from typing import Any, Optional, List, Dict
from rest_client.client import ApiClient
from .models import (
    BlockEntityResponseSchema,
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


class Entities:

    def __init__(self, client: ApiClient):
        self._client = client

    def list_entities(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[EntityResponseSchema]:
        """
        Получение списка сущностей
        """
        with allure.step("List Entities (GET /projects/{project_oid}/entities)"):
            path = f"/projects/{project_oid}/entities"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [EntityResponseSchema(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def create_entities(
        self,
        project_oid: str,
        payload: List[CreateEntityRequestSchema],
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[EntityResponseSchema]:
        """
        Создание сущностей
        """
        with allure.step("Create Entities (POST /projects/{project_oid}/entities)"):
            path = f"/projects/{project_oid}/entities"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [EntityResponseSchema(**item) for item in r_json]
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def get_entity(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityFullResponseSchema:
        """
        Получение сущности по oid
        """
        with allure.step(
            "Get Entity (GET /projects/{project_oid}/entities/{entity_oid})"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            EntityFullResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def patch_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: PatchEntityRequestSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityResponseSchema:
        """
        Изменение сущности
        """
        with allure.step(
            "Patch Entity (PATCH /projects/{project_oid}/entities/{entity_oid})"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}"

            r_json = self._client.patch(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            EntityResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def delete_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление сущности
        """
        with allure.step(
            "Delete Entity (DELETE /projects/{project_oid}/entities/{entity_oid})"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}"

            r_json = self._client.delete(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def generate_upload_urls(
        self,
        project_oid: str,
        payload: List[GenerateFileUploadLinkRequestSchema],
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[FileResponseSchema]:
        """
        Получение ссылок для загрузки файлов
        """
        with allure.step(
            "Generate Upload Urls (POST /projects/{project_oid}/entities/generate-upload-urls)"
        ):
            path = f"/projects/{project_oid}/entities/generate-upload-urls"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [FileResponseSchema(**item) for item in r_json]
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def move_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: MoveEntityRequest,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityResponseSchema:
        """
        Перемещение сущности
        """
        with allure.step(
            "Move Entity (PATCH /projects/{project_oid}/entities/{entity_oid}/move)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/move"

            r_json = self._client.patch(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            EntityResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def restore_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Восстановление сущности из архива
        """
        with allure.step(
            "Restore Entity (POST /projects/{project_oid}/entities/{entity_oid}/restore)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/restore"

            r_json = self._client.post(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def get_entity_block(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> BlockEntityResponseSchema:
        """
        Проверка, что файл не занят другим пользователем
        """
        with allure.step(
            "Get Entity Block (GET /projects/{project_oid}/entities/{entity_oid}/check)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/check"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            BlockEntityResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def block_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> BlockEntityResponseSchema:
        """
        Блокировка файла
        """
        with allure.step(
            "Block Entity (POST /projects/{project_oid}/entities/{entity_oid}/block)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/block"

            r_json = self._client.post(
                path=path, headers=headers, expected_status=expected_status
            )
        return (
            BlockEntityResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def continue_block_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Продление блокировки файла
        """
        with allure.step(
            "Continue Block Entity (POST /projects/{project_oid}/entities/{entity_oid}/block/continue)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/block/continue"

            r_json = self._client.post(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def unblock_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Разблокировка файла
        """
        with allure.step(
            "Unblock Entity (POST /projects/{project_oid}/entities/{entity_oid}/unblock)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/unblock"

            r_json = self._client.post(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def get_entity_files_download_url(
        self,
        entity_oid: str,
        project_oid: str,
        view: Optional[bool] = None,
        version_oid: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[FileResponseSchema]:
        """
        Получение ссылки на скачивание файлов определенной версии сущности из хранилища
        """
        with allure.step(
            "Get Entity Files Download Url (GET /projects/{project_oid}/entities/{entity_oid}/download)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/download"

            r_json = self._client.get(
                path=path,
                params={"view": view, "version_oid": version_oid, **(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [FileResponseSchema(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def get_entity_versions(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> List[EntityVersionListResponseSchema]:
        """
        Получение списка версий сущности
        """
        with allure.step(
            "Get Entity Versions (GET /projects/{project_oid}/entities/{entity_oid}/versions)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/versions"

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            [EntityVersionListResponseSchema(**item) for item in r_json]
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def create_entity_new_version(
        self,
        entity_oid: str,
        project_oid: str,
        payload: EntityVersionRequestSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateEntityVersionResponseSchema:
        """
        Создание новой версии сущности (прикрепление файлов новой версии)
        """
        with allure.step(
            "Create Entity New Version (POST /projects/{project_oid}/entities/{entity_oid}/versions)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/versions"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            CreateEntityVersionResponseSchema(**r_json)
            if expected_status == HTTPStatus.CREATED
            else r_json
        )

    def get_entity_version(
        self,
        version_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityVersionFullResponseSchema:
        """
        Получение версии сущности по oid
        """
        with allure.step(
            "Get Entity Version (GET /projects/{project_oid}/entities/{entity_oid}/versions/{version_oid})"
        ):
            path = (
                f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}"
            )

            r_json = self._client.get(
                path=path,
                params={**(params or {})},
                headers=headers,
                expected_status=expected_status,
            )
        return (
            EntityVersionFullResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )

    def delete_entity_version(
        self,
        entity_oid: str,
        version_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление версии сущности
        """
        with allure.step(
            "Delete Entity Version (DELETE /projects/{project_oid}/entities/{entity_oid}/versions/{version_oid})"
        ):
            path = (
                f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}"
            )

            r_json = self._client.delete(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def restore_entity_version(
        self,
        version_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Восстановление версии сущности из архива
        """
        with allure.step(
            "Restore Entity Version (POST /projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}/restore)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}/restore"

            r_json = self._client.post(
                path=path, headers=headers, expected_status=expected_status
            )
        return r_json

    def remove_files_from_storage(
        self,
        project_oid: str,
        payload: BodyRemoveFilesFromStorageProjectsProjectOidEntitiesFilesRemoveFromStoragePost,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удалить файлы из хранилища
        """
        with allure.step(
            "Remove Files From Storage (POST /projects/{project_oid}/entities/files/remove-from-storage)"
        ):
            path = f"/projects/{project_oid}/entities/files/remove-from-storage"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return r_json

    def check_content(
        self,
        entity_oid: str,
        project_oid: str,
        payload: CheckContentRequestSchema,
        headers: Optional[Dict[str, str]] = None,
        expected_status: HTTPStatus = HTTPStatus.OK,
    ) -> ContentCheckResponseSchema:
        """
        Проверка файла/модели
        """
        with allure.step(
            "Check Content (POST /projects/{project_oid}/entities/{entity_oid}/check-content)"
        ):
            path = f"/projects/{project_oid}/entities/{entity_oid}/check-content"

            r_json = self._client.post(
                path=path,
                payload=payload,
                headers=headers,
                expected_status=expected_status,
            )
        return (
            ContentCheckResponseSchema(**r_json)
            if expected_status == HTTPStatus.OK
            else r_json
        )
