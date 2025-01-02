from http import HTTPStatus
from typing import Any, Optional, List, Dict
from api_client import ApiClientServices
from models import (
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


class Entities(ApiClientServices):
    def list_entities(
        self,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[EntityResponseSchema]:
        """
        Получение списка сущностей
        """
        path = f"/projects/{project_oid}/entities"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            [EntityResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    def create_entities(
        self,
        project_oid: str,
        payload: List[CreateEntityRequestSchema],
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[EntityResponseSchema]:
        """
        Создание сущностей
        """
        path = f"/projects/{project_oid}/entities"
        r_json = self.post(
            path=path, payload=[item.dict() for item in payload], expected_status=status
        )

        return (
            [EntityResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.CREATED
            else r_json
        )

    def get_entity(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityFullResponseSchema:
        """
        Получение сущности по oid
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}"
        r_json = self.get(path=path, params=params, expected_status=status)

        return EntityFullResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    def patch_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: PatchEntityRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityResponseSchema:
        """
        Изменение сущности
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}"
        r_json = self.patch(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return EntityResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    def delete_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление сущности
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}"
        r_json = self.delete(path=path, expected_status=status)

        return r_json

    def generate_upload_urls(
        self,
        project_oid: str,
        payload: List[GenerateFileUploadLinkRequestSchema],
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> List[FileResponseSchema]:
        """
        Получение ссылок для загрузки файлов
        """
        path = f"/projects/{project_oid}/entities/generate-upload-urls"
        r_json = self.post(
            path=path, payload=[item.dict() for item in payload], expected_status=status
        )

        return (
            [FileResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.CREATED
            else r_json
        )

    def move_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: MoveEntityRequest,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityResponseSchema:
        """
        Перемещение сущности
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/move"
        r_json = self.patch(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return EntityResponseSchema(**r_json) if status == HTTPStatus.OK else r_json

    def restore_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Восстановление сущности из архива
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/restore"
        r_json = self.post(path=path, expected_status=status)

        return r_json

    def get_entity_block(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> BlockEntityResponseSchema:
        """
        Проверка, что файл не занят другим пользователем
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/check"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            BlockEntityResponseSchema(**r_json) if status == HTTPStatus.OK else r_json
        )

    def block_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> BlockEntityResponseSchema:
        """
        Блокировка файла
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/block"
        r_json = self.post(path=path, expected_status=status)

        return (
            BlockEntityResponseSchema(**r_json) if status == HTTPStatus.OK else r_json
        )

    def continue_block_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Продление блокировки файла
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/block/continue"
        r_json = self.post(path=path, expected_status=status)

        return r_json

    def unblock_entity(
        self,
        entity_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Разблокировка файла
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/unblock"
        r_json = self.post(path=path, expected_status=status)

        return r_json

    def get_entity_files_download_url(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[FileResponseSchema]:
        """
        Получение ссылки на скачивание файлов определенной версии сущности из хранилища
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/download"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            [FileResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    def get_entity_versions(
        self,
        entity_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> List[EntityVersionListResponseSchema]:
        """
        Получение списка версий сущности
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/versions"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            [EntityVersionListResponseSchema(**item) for item in r_json]
            if status == HTTPStatus.OK
            else r_json
        )

    def create_entity_new_version(
        self,
        entity_oid: str,
        project_oid: str,
        payload: EntityVersionRequestSchema,
        status: HTTPStatus = HTTPStatus.CREATED,
    ) -> CreateEntityVersionResponseSchema:
        """
        Создание новой версии сущности (прикрепление файлов новой версии)
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/versions"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            CreateEntityVersionResponseSchema(**r_json)
            if status == HTTPStatus.CREATED
            else r_json
        )

    def get_entity_version(
        self,
        version_oid: str,
        project_oid: str,
        params: Optional[Dict[str, Any]] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> EntityVersionFullResponseSchema:
        """
        Получение версии сущности по oid
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}"
        r_json = self.get(path=path, params=params, expected_status=status)

        return (
            EntityVersionFullResponseSchema(**r_json)
            if status == HTTPStatus.OK
            else r_json
        )

    def delete_entity_version(
        self,
        entity_oid: str,
        version_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удаление версии сущности
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}"
        r_json = self.delete(path=path, expected_status=status)

        return r_json

    def restore_entity_version(
        self,
        version_oid: str,
        project_oid: str,
        payload: Optional[Any] = None,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> Any:
        """
        Восстановление версии сущности из архива
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/versions/{version_oid}/restore"
        r_json = self.post(path=path, expected_status=status)

        return r_json

    def remove_files_from_storage(
        self,
        project_oid: str,
        payload: BodyRemoveFilesFromStorageProjectsProjectOidEntitiesFilesRemoveFromStoragePost,
        status: HTTPStatus = HTTPStatus.NO_CONTENT,
    ) -> Any:
        """
        Удалить файлы из хранилища
        """
        path = f"/projects/{project_oid}/entities/files/remove-from-storage"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return r_json

    def check_content(
        self,
        entity_oid: str,
        project_oid: str,
        payload: CheckContentRequestSchema,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> ContentCheckResponseSchema:
        """
        Проверка файла/модели
        """
        path = f"/projects/{project_oid}/entities/{entity_oid}/check-content"
        r_json = self.post(
            path=path,
            payload=payload.dict() if payload else None,
            expected_status=status,
        )

        return (
            ContentCheckResponseSchema(**r_json) if status == HTTPStatus.OK else r_json
        )
