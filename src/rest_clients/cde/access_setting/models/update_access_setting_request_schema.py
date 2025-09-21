"""Generated model: UpdateAccessSettingRequestSchema."""

from pydantic_utils.pydantic_config import BaseConfigModel
from uuid import UUID
from typing import List, Optional


class UpdateAccessSettingRequestSchema(BaseConfigModel):
    update_role_groups: Optional[List[UpdateRoleGroupAccessSettingSchema]] = None
    """Ролевые группы на выдачу доступа"""
    update_users: Optional[List[UpdateUserAccessSettingSchema]] = None
    """Пользователи(UUID) на выдачу доступа"""
    remove_role_groups: Optional[List[UUID]] = None
    """Ролевые группы (UUID) на удаление доступа"""
    remove_users: Optional[List[UUID]] = None
    """Пользователи (UUID) на удаление доступа"""
