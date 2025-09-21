import os
import re
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
from codegen.data_models import Endpoint, MethodContext


class ClientGenerator:
    def __init__(
        self, endpoints: List[Endpoint], imports: List[str], template_name: str
    ):
        self.endpoints = endpoints
        self.imports = imports
        self.template = self._load_template(template_name)

    def _load_template(self, template_name: str):
        # Get absolute path to templates directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, "templates")
        templates_path = os.path.abspath(templates_dir)

        env = Environment(
            loader=FileSystemLoader(templates_path),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        return env.get_template(template_name)

    def generate_clients(
        self, output_dir: str, module_name: str, service_path: str
    ) -> Dict[str, str]:
        """Generate client files, grouping endpoints by tags"""
        os.makedirs(output_dir, exist_ok=True)

        grouped_endpoints = self._group_endpoints_by_tag()
        file_to_class = {}

        for tag, endpoints in grouped_endpoints.items():
            class_name = self._tag_to_class_name(tag)
            file_name = f"{class_name.lower()}_client.py"

            self._generate_client_file(
                endpoints, class_name, file_name, output_dir, module_name, service_path
            )

            file_to_class[file_name] = class_name

        return file_to_class

    def _group_endpoints_by_tag(self) -> Dict[str, List[Endpoint]]:
        """Group endpoints by tags"""
        grouped = {}
        for endpoint in self.endpoints:
            grouped.setdefault(endpoint.tag, []).append(endpoint)
        return grouped

    def _tag_to_class_name(self, tag: str) -> str:
        """Convert tag to class name: 'user-management' -> 'UserManagement'"""
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
        """Generate client file"""
        method_contexts = [MethodContext.from_endpoint(ep) for ep in endpoints]

        rendered_content = self.template.render(
            class_name=class_name,
            service_path=service_path,
            methods=method_contexts,
            models_import_path=f"http_clients.{module_name}.models",
            imports=self.imports,
        )

        file_path = os.path.join(output_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rendered_content)
