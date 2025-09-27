"""Utilities for generating placeholder test structure."""

import os
import re
from typing import Dict, List, Set, Tuple

from codegen.data_models import Endpoint
from dto_parser.schema_parser import ModelDefinition
from utils.naming import to_snake_case


class TestsGenerator:
    """Generate skeletal test folders mirroring service clients."""

    def __init__(
        self,
        base_dir: str,
        package_root: str,
        model_definitions: Dict[str, ModelDefinition],
    ) -> None:
        self.base_dir = base_dir
        self.package_root = package_root
        self.model_definitions: Dict[str, ModelDefinition] = model_definitions

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

            asserts_dir = os.path.join(module_dir, "asserts")
            os.makedirs(asserts_dir, exist_ok=True)
            self._ensure_init(asserts_dir)

            self._create_placeholder_test(
                module_dir,
                asserts_dir,
                service_name,
                module_name,
                class_name,
                endpoints,
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
        asserts_dir: str,
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
                {
                    "method_name": method_name,
                    "http_method": endpoint.http_method.upper(),
                    "path": endpoint.path,
                    "description": endpoint.summary
                    or endpoint.description
                    or endpoint.name,
                    "endpoint": endpoint,
                    **self._analyze_return(endpoint),
                }
            )

        if not endpoint_tests:
            endpoint_tests.append(
                {
                    "method_name": f"{module_name}_placeholder",
                    "http_method": "",
                    "path": "",
                    "description": f"Add tests for {class_name}",
                    "endpoint": None,
                    "placeholder": True,
                }
            )

        assert_imports = []
        tests_body = []
        for entry in endpoint_tests:
            method_name = entry["method_name"]
            http_method = entry["http_method"]
            path = entry["path"]
            description = entry["description"].replace("\"", "\'")
            placeholder = entry.get("placeholder", False)
            endpoint = entry.get("endpoint")
            is_list = entry.get("is_list", False)
            is_optional = entry.get("is_optional", False)

            http_info = f"{http_method} {path}".strip()
            skip_message = (
                f"Add tests for {service_name}.{module_name}.{method_name}"
                if not http_info
                else f"Add tests for {service_name}.{module_name}.{method_name} ({http_info})"
            )

            if not placeholder:
                model_names = self._resolve_return_models(endpoint)
                self._create_assert_file(
                    asserts_dir,
                    service_name,
                    module_name,
                    class_name,
                    method_name,
                    http_method,
                    path,
                    description,
                    model_names,
                    is_list,
                    is_optional,
                )
                assert_imports.append(
                    f"from .asserts.assert_{method_name} import assert_{method_name}"
                )

                tests_body.append(
                    f"@pytest.mark.skip(\"{skip_message}\")\n"
                    f"def test_{method_name}() -> None:\n"
                    f"    \"\"\"Auto-generated placeholder for {class_name}.{method_name}: {description}.\"\"\"\n"
                    f"    response = ...  # TODO: invoke endpoint\n"
                    f"    assert_{method_name}(response)\n"
                )
            else:
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

        asserts_import_block = "\n".join(assert_imports)
        if asserts_import_block:
            asserts_import_block += "\n\n"

        content = (
            f"\"\"\"Placeholder tests for {class_name}.\"\"\"\n\n"
            "import pytest\n\n"
            + imports
            + asserts_import_block
            + "\n".join(tests_body)
            + "\n"
        )

        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)

    def _create_assert_file(
        self,
        asserts_dir: str,
        service_name: str,
        module_name: str,
        class_name: str,
        method_name: str,
        http_method: str,
        path: str,
        description: str,
        model_names: List[str],
        is_list: bool,
        is_optional: bool,
    ) -> None:
        file_path = os.path.join(asserts_dir, f"assert_{method_name}.py")
        if os.path.exists(file_path):
            return

        http_info = f"{http_method} {path}".strip()
        doc_line = (
            f"{http_info}" if http_info else f"Assertions for {class_name}.{method_name}"
        )

        content_lines = [
            f"\"\"\"Assertions for {class_name}.{method_name}.",
            f"Endpoint: {doc_line}.\"\"\"\n",
            "from rest_generator.utils.assertions import expect\n",
            f"def assert_{method_name}(response) -> None:",
            f"    \"\"\"Validate response for {class_name}.{method_name}: {description}.\"\"\"",
        ]

        content_lines.extend(
            self._build_response_assertions(model_names, is_list, is_optional)
        )

        content = "\n".join(content_lines) + "\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _resolve_return_models(self, endpoint: Endpoint) -> List[str]:
        if not endpoint or not endpoint.return_type:
            return []

        candidates = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", endpoint.return_type)
        models = []
        for name in candidates:
            if name in self.model_definitions and name not in models:
                models.append(name)
        return models

    def _analyze_return(self, endpoint: Endpoint) -> Dict[str, bool]:
        return_type = endpoint.return_type or ""
        return {
            "is_list": "List[" in return_type or "list[" in return_type.lower(),
            "is_optional": "Optional[" in return_type,
        }

    def _build_response_assertions(
        self, model_names: List[str], is_list: bool, is_optional: bool
    ) -> List[str]:
        lines: List[str] = ["    expect(response, \"response\").is_not_none()"]

        if is_optional:
            lines.append(
                "    # NOTE: response is optional in schema; adjust checks if None is valid"
            )

        visited: Set[str] = set()

        if is_list:
            lines.append("    expect(response, \"response\").is_not_empty()")
            lines.append("    item = response[0]  # TODO: adjust indexing if needed")
            if model_names:
                primary_model = model_names[0]
                if primary_model in self.model_definitions:
                    lines.extend(
                        self._build_field_expectations(
                            primary_model,
                            prefix="item",
                            path_prefix="response[0]",
                            visited=visited,
                            indent="    ",
                        )
                    )
            return lines

        if model_names:
            primary_model = model_names[0]
            if primary_model in self.model_definitions:
                lines.extend(
                    self._build_field_expectations(
                        primary_model,
                        prefix="response",
                        path_prefix="response",
                        visited=visited,
                        indent="    ",
                    )
                )

        return lines

    def _build_field_expectations(
        self,
        model_name: str,
        prefix: str,
        path_prefix: str,
        visited: set[str],
        indent: str,
    ) -> List[str]:
        if model_name in visited:
            return []

        visited = set(visited)
        visited.add(model_name)

        model_def = self.model_definitions.get(model_name)
        if not model_def or not model_def.fields:
            return []

        lines: List[str] = []
        for field in model_def.fields:
            base_type, is_list, is_optional = self._parse_type(field.type_str)
            field_expr = f"{prefix}.{field.name}"
            field_path = f"{path_prefix}.{field.name}"

            if is_optional:
                lines.append(
                    f"{indent}# Field '{field.name}' is optional; add extra checks if None is valid"
                )
                lines.append(f"{indent}if {field_expr} is not None:")
                lines.extend(
                    self._build_expectations_for_type(
                        base_type,
                        is_list,
                        field_expr,
                        field_path,
                        visited,
                        indent + "    ",
                    )
                )
            else:
                lines.extend(
                    self._build_expectations_for_type(
                        base_type,
                        is_list,
                        field_expr,
                        field_path,
                        visited,
                        indent,
                    )
                )

        return lines

    def _build_expectations_for_type(
        self,
        base_type: str,
        is_list: bool,
        field_expr: str,
        field_path: str,
        visited: set[str],
        indent: str,
    ) -> List[str]:
        lines: List[str] = []

        if base_type in self.model_definitions:
            if is_list:
                lines.append(
                    f"{indent}expect({field_expr}, \"{field_path}\").is_not_empty()"
                )
                item_var = field_expr.split(".")[-1] + "_item"
                lines.append(
                    f"{indent}{item_var} = {field_expr}[0]  # TODO: iterate over all items"
                )
                lines.extend(
                    self._build_field_expectations(
                        base_type,
                        prefix=item_var,
                        path_prefix=f"{field_path}[0]",
                        visited=visited,
                        indent=indent + "    ",
                    )
                )
            else:
                lines.append(
                    f"{indent}expect({field_expr}, \"{field_path}\").is_not_none()"
                )
                lines.extend(
                    self._build_field_expectations(
                        base_type,
                        prefix=field_expr,
                        path_prefix=field_path,
                        visited=visited,
                        indent=indent,
                    )
                )
            return lines

        # Primitive or unknown type
        if is_list:
            lines.append(
                f"{indent}expect({field_expr}, \"{field_path}\").is_not_empty()"
            )
        else:
            lines.append(
                f"{indent}expect({field_expr}, \"{field_path}\").is_not_none()"
            )

        return lines

    def _parse_type(self, type_str: str) -> Tuple[str, bool, bool]:
        clean = (type_str or "").replace(" ", "")
        optional = False
        while clean.startswith("Optional[") and clean.endswith("]"):
            optional = True
            clean = clean[len("Optional[") : -1]

        is_list = False
        if clean.startswith("List[") and clean.endswith("]"):
            is_list = True
            clean = clean[5:-1]
        elif clean.startswith("list[") and clean.endswith("]"):
            is_list = True
            clean = clean[5:-1]

        # Strip nested optional after list handling
        while clean.startswith("Optional[") and clean.endswith("]"):
            clean = clean[len("Optional[") : -1]

        return clean, is_list, optional
