"""Client generator for creating REST API client classes."""

import os
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List

from jinja2 import Environment, FileSystemLoader

from codegen.data_models import Endpoint, MethodContext


class IClientGenerator(ABC):
    """Interface for client generators."""

    @abstractmethod
    def generate_clients(
        self, output_dir: str, module_name: str, service_path: str
    ) -> Dict[str, str]:
        """Generate client files."""
        pass


class ClientGenerator(IClientGenerator):
    """Generates REST API client classes from endpoint definitions."""
    def __init__(
        self, endpoints: List[Endpoint], imports: List[str], template_name: str
    ) -> None:
        """Initialize the client generator.

        Args:
            endpoints: List of API endpoints to generate clients for
            imports: List of additional imports needed by the generated clients
            template_name: Name of the Jinja2 template file to use

        Raises:
            TypeError: If endpoints or imports are not lists
            ValueError: If template_name is empty
        """
        if not isinstance(endpoints, list):
            raise TypeError("endpoints must be a list")
        if not isinstance(imports, list):
            raise TypeError("imports must be a list")
        if not template_name.strip():
            raise ValueError("template_name cannot be empty")

        self._endpoints = endpoints
        self._imports = imports
        self._template = self._load_template(template_name)

    def _load_template(self, template_name: str):
        """Load the Jinja2 template.

        Args:
            template_name: Name of the template file

        Returns:
            Loaded Jinja2 template

        Raises:
            FileNotFoundError: If template file is not found
        """
        # Get absolute path to templates directory
        current_dir = Path(__file__).parent
        templates_dir = current_dir / "templates"
        templates_path = templates_dir.resolve()

        try:
            env = Environment(
                loader=FileSystemLoader(str(templates_path)),
                trim_blocks=True,
                lstrip_blocks=True,
            )
            return env.get_template(template_name)
        except Exception as e:
            raise FileNotFoundError(f"Template {template_name} not found: {e}") from e

    def generate_clients(
        self, output_dir: str, module_name: str, service_path: str
    ) -> Dict[str, str]:
        """Generate client files, grouping endpoints by tags.

        Args:
            output_dir: Directory to write generated client files
            module_name: Name of the module for imports
            service_path: Base service path for endpoints

        Returns:
            Dictionary mapping file names to class names

        Raises:
            ValueError: If any parameter is empty
        """
        if not output_dir.strip():
            raise ValueError("output_dir cannot be empty")
        if not module_name.strip():
            raise ValueError("module_name cannot be empty")

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        grouped_endpoints = self._group_endpoints_by_tag()
        file_to_class_mapping = {}

        for tag, endpoints in grouped_endpoints.items():
            class_name = self._tag_to_class_name(tag)
            file_name = f"{class_name.lower()}_client.py"

            self._generate_client_file(
                endpoints, class_name, file_name, output_dir, module_name, service_path
            )

            file_to_class_mapping[file_name] = class_name

        return file_to_class_mapping

    def _group_endpoints_by_tag(self) -> Dict[str, List[Endpoint]]:
        """Group endpoints by tags.

        Returns:
            Dictionary mapping tags to lists of endpoints
        """
        grouped: Dict[str, List[Endpoint]] = {}
        for endpoint in self._endpoints:
            grouped.setdefault(endpoint.tag, []).append(endpoint)
        return grouped

    def _tag_to_class_name(self, tag: str) -> str:
        """Convert tag to class name: 'user-management' -> 'UserManagement'.

        Args:
            tag: The tag string to convert

        Returns:
            PascalCase class name

        Raises:
            ValueError: If tag is empty
        """
        if not tag.strip():
            raise ValueError("tag cannot be empty")

        normalized_tag = tag.replace("-", "_")
        parts = re.split(r"[\s_]+", normalized_tag)
        return "".join(word.capitalize() for word in parts if word)

    def _generate_client_file(
        self,
        endpoints: List[Endpoint],
        class_name: str,
        file_name: str,
        output_dir: str,
        module_name: str,
        service_path: str,
    ) -> None:
        """Generate client file.

        Args:
            endpoints: List of endpoints for this client
            class_name: Name of the client class
            file_name: Name of the output file
            output_dir: Directory to write the file
            module_name: Module name for imports
            service_path: Base service path
        """
        method_contexts = [MethodContext.from_endpoint(ep) for ep in endpoints]

        rendered_content = self._template.render(
            class_name=class_name,
            service_path=service_path,
            methods=method_contexts,
            models_import_path=f"http_clients.{module_name}.models",
            imports=self._imports,
        )

        file_path = Path(output_dir) / file_name
        file_path.write_text(rendered_content, encoding="utf-8")
