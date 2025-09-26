"""Utilities for generating placeholder test structure."""

import os
from typing import Dict, List

from codegen.data_models import Endpoint
from utils.naming import to_snake_case


class TestsGenerator:
    """Generate skeletal test folders mirroring service clients."""

    def __init__(self, base_dir: str, package_root: str) -> None:
        self.base_dir = base_dir
        self.package_root = package_root

    def generate(
        self,
        service_name: str,
        file_to_class: Dict[str, str],
        module_endpoints: Dict[str, List[Endpoint]],
    ) -> None:
        """Create directories and placeholder tests for a service."""
        if not file_to_class:
            return

        service_dir = os.path.join(self.base_dir, service_name)
        os.makedirs(service_dir, exist_ok=True)

        self._ensure_init(self.base_dir)
        self._ensure_init(service_dir)

        for module_name in sorted(file_to_class):
            class_name = file_to_class[module_name]
            endpoints = module_endpoints.get(module_name, [])
            module_dir = os.path.join(service_dir, module_name)
            os.makedirs(module_dir, exist_ok=True)
            self._ensure_init(module_dir)
            self._create_placeholder_test(
                module_dir, service_name, module_name, class_name, endpoints
            )

    def _ensure_init(self, directory: str) -> None:
        init_file = os.path.join(directory, "__init__.py")
        if os.path.exists(init_file):
            return
        with open(init_file, "w", encoding="utf-8") as f:
            f.write('"""Package marker."""\n')

    def _create_placeholder_test(
        self,
        module_dir: str,
        service_name: str,
        module_name: str,
        class_name: str,
        endpoints: List[Endpoint],
    ) -> None:
        test_file = os.path.join(module_dir, f"test_{module_name}.py")
        if os.path.exists(test_file):
            return

        endpoint_tests = []
        seen_names = set()
        for endpoint in endpoints:
            method_name = to_snake_case(endpoint.name)
            if method_name in seen_names:
                suffix = 2
                while f"{method_name}_{suffix}" in seen_names:
                    suffix += 1
                method_name = f"{method_name}_{suffix}"
            seen_names.add(method_name)
            endpoint_tests.append(
                (
                    method_name,
                    endpoint.http_method.upper(),
                    endpoint.path,
                    endpoint.summary or endpoint.description or endpoint.name,
                )
            )

        if not endpoint_tests:
            endpoint_tests.append(
                (
                    f"{module_name}_placeholder",
                    "",
                    "",
                    f"Add tests for {class_name}",
                )
            )

        tests_body = []
        for method_name, http_method, path, doc in endpoint_tests:
            description = doc.replace("\"", "\'")
            http_info = f"{http_method} {path}".strip()
            skip_message = (
                f"Add tests for {service_name}.{module_name}.{method_name}"
                if not http_info
                else f"Add tests for {service_name}.{module_name}.{method_name} ({http_info})"
            )
            tests_body.append(
                f"@pytest.mark.skip(\"{skip_message}\")\n"
                f"def test_{method_name}() -> None:\n"
                f"    \"\"\"Auto-generated placeholder for {class_name}.{method_name}: {description}.\"\"\"\n"
                f"    ...\n"
            )

        imports = (
            f"from {self.package_root}.{service_name}.{module_name}.client import {class_name}  # noqa: F401\n\n"
            if service_name
            else ""
        )

        content = (
            f"\"\"\"Placeholder tests for {class_name}.\"\"\"\n\n"
            "import pytest\n\n"
            + imports
            + "\n".join(tests_body)
            + "\n"
        )

        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)
