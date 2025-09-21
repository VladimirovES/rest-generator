"""Generated model: Body_remove_files_from_storage_projects__project_oid__entities_files_remove_from_storage_post."""

from pydantic_utils.pydantic_config import BaseConfigModel
from typing import List


class Body_remove_files_from_storage_projects__project_oid__entities_files_remove_from_storage_post(
    BaseConfigModel
):
    files: List[FileRequestSchema]
