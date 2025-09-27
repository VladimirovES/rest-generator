"""Generator for assertion helper modules built on top of expect()."""

import os
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple

from dto_parser.schema_parser import ModelDefinition

from codegen.data_models import Endpoint
from codegen.endpoint_metadata import EndpointInfo, build_endpoint_info


@dataclass(frozen=True)
class ModuleAssertions:
    """Container describing generated assertion helpers for a module."""

    module_name: str
    methods: Tuple[str, ...]


class AssertsGenerator:
    """Generate reusable assert helpers for each generated endpoint."""

    def __init__(self, base_dir: str, model_definitions: Dict[str, ModelDefinition]):
        self.base_dir = base_dir
        self.model_definitions = model_definitions

    def generate(
        self, service_name: str, module_endpoints: Dict[str, List[Endpoint]]
    ) -> List[ModuleAssertions]:
        """Create assert modules and describe them with dataclasses."""

        results: List[ModuleAssertions] = []

        service_dir = os.path.join(self.base_dir, service_name)
        os.makedirs(service_dir, exist_ok=True)
        self._ensure_init(self.base_dir)
        self._ensure_init(service_dir)

        for module_name in sorted(module_endpoints):
            infos = build_endpoint_info(module_endpoints[module_name])
            if not infos:
                continue

            module_dir = os.path.join(service_dir, module_name)
            os.makedirs(module_dir, exist_ok=True)
            self._ensure_init(module_dir)

            asserts_dir = os.path.join(module_dir, "asserts")
            os.makedirs(asserts_dir, exist_ok=True)
            self._ensure_init(asserts_dir)

            created: List[str] = []
            for info in infos:
                self._create_assert_file(asserts_dir, module_name, info)
                created.append(info.method_name)

            if created:
                results.append(
                    ModuleAssertions(
                        module_name=module_name,
                        methods=tuple(sorted(created)),
                    )
                )

        return results

    def _ensure_init(self, directory: str) -> None:
        init_file = os.path.join(directory, "__init__.py")
        if os.path.exists(init_file):
            return
        with open(init_file, "w", encoding="utf-8") as f:
            f.write('"""Package marker."""\n')

    def _create_assert_file(
        self,
        asserts_dir: str,
        module_name: str,
        info: EndpointInfo,
    ) -> None:
        file_path = os.path.join(asserts_dir, f"assert_{info.method_name}.py")

        http_info = f"{info.http_method} {info.path}".strip()
        doc_line = http_info or f"Assertions for {module_name}.{info.method_name}"

        lines = [
            f"\"\"\"Assertions for {module_name}.{info.method_name}.",
            f"Endpoint: {doc_line}.\"\"\"\n",
            "from rest_generator.utils.assertions import expect\n",
            f"def assert_{info.method_name}(response) -> None:",
            f"    \"\"\"Validate response for {module_name}.{info.method_name}: {info.description}.\"\"\"",
        ]

        lines.extend(self._build_response_assertions(info))

        content = "\n".join(lines) + "\n"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _build_response_assertions(self, info: EndpointInfo) -> List[str]:
        lines: List[str] = ["    expect(response, \"response\").is_not_none()"]

        if info.endpoint is None:
            return lines

        base_type, is_list, is_optional = self._parse_return_type(info.endpoint.return_type)

        visited: Set[str] = set()

        if is_optional:
            lines.append(
                "    # NOTE: response is optional in schema; adjust checks if None is valid"
            )

        if is_list:
            lines.append("    expect(response, \"response\").is_not_empty()")
            lines.append("    item = response[0]  # TODO: iterate over all items")
            if base_type and base_type in self.model_definitions:
                lines.extend(
                    self._build_field_expectations(
                        base_type,
                        prefix="item",
                        path_prefix="response[0]",
                        visited=visited,
                        indent="    ",
                    )
                )
        elif base_type and base_type in self.model_definitions:
            lines.extend(
                self._build_field_expectations(
                    base_type,
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
        visited: Set[str],
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
                    f"{indent}# Field '{field.name}' is optional; adjust assertions if None is valid"
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
        visited: Set[str],
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

        if is_list:
            lines.append(
                f"{indent}expect({field_expr}, \"{field_path}\").is_not_empty()"
            )
        else:
            lines.append(
                f"{indent}expect({field_expr}, \"{field_path}\").is_not_none()"
            )

        return lines

    def _parse_return_type(self, return_type: str) -> Tuple[str, bool, bool]:
        base, is_list, is_optional = self._parse_type(return_type)
        return base, is_list, is_optional

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

        while clean.startswith("Optional[") and clean.endswith("]"):
            clean = clean[len("Optional[") : -1]

        return clean, is_list, optional
