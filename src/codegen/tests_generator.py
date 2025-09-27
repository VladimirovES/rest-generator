"""Generator for pytest placeholders referencing generated clients."""

import os
from typing import Dict, List, Optional

from codegen.data_models import Endpoint
from codegen.endpoint_metadata import EndpointInfo, build_endpoint_info


class TestsGenerator:
    """Generate pytest stubs mirroring the service/client structure."""

    def __init__(
        self,
        base_dir: str,
        package_root: str,
        include_asserts: bool,
    ) -> None:
        self.base_dir = base_dir
        self.package_root = package_root
        self.include_asserts = include_asserts

    def generate(
        self,
        service_name: str,
        file_to_class: Dict[str, str],
        module_endpoints: Dict[str, List[Endpoint]],
        module_asserts: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        module_asserts = module_asserts or {}

        service_dir = os.path.join(self.base_dir, service_name)
        os.makedirs(service_dir, exist_ok=True)
        self._ensure_init(self.base_dir)
        self._ensure_init(service_dir)

        for module_name in sorted(file_to_class):
            class_name = file_to_class[module_name]
            module_dir = os.path.join(service_dir, module_name)
            os.makedirs(module_dir, exist_ok=True)
            self._ensure_init(module_dir)

            test_file = os.path.join(module_dir, f"test_{module_name}.py")
            if os.path.exists(test_file):
                continue

            entries = build_endpoint_info(module_endpoints.get(module_name, []))
            if not entries:
                placeholder = EndpointInfo(
                    method_name=f"{module_name}_placeholder",
                    http_method="",
                    path="",
                    description=f"Add tests for {class_name}",
                    endpoint=None,
                )
                entries = [placeholder]

            content = self._render_test_file(
                service_name,
                module_name,
                class_name,
                entries,
                module_asserts.get(module_name, []),
            )

            with open(test_file, "w", encoding="utf-8") as f:
                f.write(content)

    def _render_test_file(
        self,
        service_name: str,
        module_name: str,
        class_name: str,
        entries: List[EndpointInfo],
        asserts_methods: List[str],
    ) -> str:
        lines: List[str] = []

        lines.append(f"\"\"\"Pytest placeholders for {class_name}.\"\"\"")
        lines.append("")
        lines.append("import pytest")

        client_import = (
            f"from {self.package_root}.{service_name}.{module_name}.client import {class_name}  # noqa: F401"
        )
        lines.append(client_import)

        include_assert_calls = self.include_asserts and bool(asserts_methods)

        if include_assert_calls:
            for method in sorted(asserts_methods):
                lines.append(
                    f"from .asserts.assert_{method} import assert_{method}"
                )

        lines.append("")

        for entry in entries:
            http_info = f"{entry.http_method} {entry.path}".strip()
            skip_reason = (
                f"Add tests for {service_name}.{module_name}.{entry.method_name}"
                if not http_info
                else f"Add tests for {service_name}.{module_name}.{entry.method_name} ({http_info})"
            )

            lines.append(f"@pytest.mark.skip(\"{skip_reason}\")")
            lines.append(f"def test_{entry.method_name}() -> None:")
            lines.append(
                f"    \"\"\"Auto-generated placeholder for {class_name}.{entry.method_name}: {entry.description}.\"\"\""
            )

            if include_assert_calls and entry.method_name in asserts_methods:
                lines.append("    response = ...  # TODO: invoke endpoint")
                lines.append(f"    assert_{entry.method_name}(response)")
            else:
                lines.append("    ...")

            lines.append("")

        return "\n".join(lines)

    def _ensure_init(self, directory: str) -> None:
        init_file = os.path.join(directory, "__init__.py")
        if os.path.exists(init_file):
            return
        with open(init_file, "w", encoding="utf-8") as f:
            f.write('"""Package marker."""\n')
