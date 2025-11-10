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
from utils.naming import to_snake_case


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
        """Имя папки/модуля - только из title с правильным snake_case

        Examples:
            "Atom Aftersales OnlineBookingService WebApi" -> "atom_aftersales_online_booking_service_webapi"
            "Atom Aftersales WarrantyService WebApi" -> "atom_aftersales_warranty_service_webapi"
        """
        title = self.swagger_spec.info.title

        # Split by spaces and special characters to get words/components
        words = re.split(r"[^a-zA-Z0-9]+", title.strip())

        # Convert each word to snake_case (handles CamelCase words)
        snake_parts = []
        for word in words:
            if word:  # Skip empty strings
                snake_word = to_snake_case(word)
                snake_parts.append(snake_word)

        # Join all parts with underscore
        return "_".join(snake_parts)

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
