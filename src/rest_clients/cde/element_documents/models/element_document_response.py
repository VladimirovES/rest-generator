"""Generated model: ElementDocumentResponse."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List


class ElementDocumentResponse(BaseConfigModel):
    project_oid: UUID
    """UUID проекта"""
    entity_version_oid: UUID
    """UUID версии сущности"""
    element_oid: str
    """UUID элемента"""
    documents: List[DocumentResponse]
    """Список документов"""
