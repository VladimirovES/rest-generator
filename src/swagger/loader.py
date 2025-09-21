"""Utilities for loading Swagger/OpenAPI specifications."""

import json
import re
import shutil
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from pydantic import ValidationError

from utils.shell import run_command
from swagger.swagger_models import SwaggerSpec


class SwaggerLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.swagger_spec: Optional[SwaggerSpec] = None

    def load(self) -> None:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                swagger_dict = json.load(f)
            self.swagger_spec = SwaggerSpec(**swagger_dict)
        except ValidationError as e:
            raise ValueError(f"Invalid swagger format: {e}")

    def get_module_name(self) -> str:
        """Имя папки/модуля - только из title"""
        title = self.swagger_spec.info.title
        normalized = re.sub(r"[^a-zA-Z0-9]+", "_", title.strip())
        return normalized.lower().strip("_")

    def get_service_path(self) -> str:
        """Путь сервиса для URL - из servers"""
        if self.swagger_spec.servers:
            return self.swagger_spec.servers[0].url
        return "/"

    def download_swagger(self, url: str) -> None:
        """Download the swagger specification to the configured file path."""
        destination = Path(self.file_path)
        parsed = urlparse(url)

        # Handle file:// URLs (or plain local paths) without invoking curl
        if parsed.scheme in {"", "file"}:
            source_path = Path(parsed.path or url)

            # If curl would overwrite the same file, skip copying
            if source_path.resolve() == destination.resolve():
                return

            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, destination)
            return

        # Fallback to curl for remote URLs
        destination.parent.mkdir(parents=True, exist_ok=True)
        swagger_cmd = f"curl -L {url!r} -o {str(destination)!r}"
        run_command(swagger_cmd)
