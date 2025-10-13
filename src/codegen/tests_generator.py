"""Generator for pytest placeholders referencing generated clients."""

import os
from pathlib import Path
from typing import Dict, List, Optional, Set

from codegen.asserts_generator import ModuleAssertions
from codegen.data_models import Endpoint, MethodContext
from codegen.endpoint_metadata import EndpointInfo, build_endpoint_info


class TestsGenerator:
    """Generate pytest stubs mirroring the service/client structure with function signatures."""

    def __init__(
        self,
        base_dir: str,
        package_root: str,
        include_asserts: bool,
        facade_class_name: Optional[str] = None,
    ) -> None:
        """Initialize the test generator.

        Args:
            base_dir: Base directory for test files
            package_root: Root package name for imports
            include_asserts: Whether to include assertion helpers
            facade_class_name: Name of the facade class for object chains
        """
        self.base_dir = Path(base_dir)
        self.package_root = package_root
        self.include_asserts = include_asserts
        self.facade_class_name = facade_class_name or "ApiClient"

    def generate(
        self,
        service_name: str,
        file_to_class: Dict[str, str],
        module_endpoints: Dict[str, List[Endpoint]],
        module_asserts: Optional[List[ModuleAssertions]] = None,
    ) -> None:
        """Generate test files with function signatures and facade chains.

        Args:
            service_name: Name of the service
            file_to_class: Mapping of module names to class names
            module_endpoints: Mapping of module names to their endpoints
            module_asserts: Optional assertion helpers
        """
        asserts_map = {
            item.module_name: set(item.methods) for item in (module_asserts or [])
        }

        service_dir = self.base_dir / service_name
        service_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_init_file(self.base_dir)
        self._ensure_init_file(service_dir)

        for module_name in sorted(file_to_class):
            class_name = file_to_class[module_name]
            module_dir = service_dir / module_name
            module_dir.mkdir(parents=True, exist_ok=True)
            self._ensure_init_file(module_dir)

            test_file = module_dir / f"test_{module_name}.py"
            if test_file.exists():
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
                asserts_map.get(module_name, set()),
            )

            test_file.write_text(content, encoding="utf-8")

    def _render_test_file(
        self,
        service_name: str,
        module_name: str,
        class_name: str,
        entries: List[EndpointInfo],
        asserts_methods: Set[str],
    ) -> str:
        """Render test file with function signatures and facade chains.

        Args:
            service_name: Name of the service
            module_name: Name of the module
            class_name: Name of the client class
            entries: List of endpoint information
            asserts_methods: Set of available assertion methods

        Returns:
            Generated test file content
        """
        lines: List[str] = []

        lines.append(f"\"\"\"Pytest placeholders for {class_name} with function signatures.\"\"\"")
        lines.append("")
        lines.append("import pytest")
        lines.append("from typing import Any, Dict, Optional")
        lines.append("")

        # Import the client class
        client_import = (
            f"from {self.package_root}.{service_name}.{module_name}.client import {class_name}"
        )
        lines.append(client_import)

        # Import facade if available
        facade_import = (
            f"# from {self.package_root}.{service_name} import {self.facade_class_name}  # Uncomment if using facade"
        )
        lines.append(facade_import)

        include_assert_calls = self.include_asserts and bool(asserts_methods)

        if include_assert_calls:
            for method in sorted(asserts_methods):
                lines.append(
                    f"from .asserts.assert_{method} import assert_{method}"
                )

        lines.append("")

        for entry in entries:
            if entry.endpoint:
                self._add_endpoint_test(lines, entry, service_name, module_name, class_name, include_assert_calls, asserts_methods)
            else:
                self._add_placeholder_test(lines, entry, service_name, module_name, class_name)

            lines.append("")

        return "\n".join(lines)

    def _ensure_init_file(self, directory: Path) -> None:
        """Ensure __init__.py exists in the directory.

        Args:
            directory: Directory path where __init__.py should be created
        """
        init_file = directory / "__init__.py"
        if init_file.exists():
            return
        init_file.write_text('"""Package marker."""\n', encoding="utf-8")

    def _add_endpoint_test(
        self,
        lines: List[str],
        entry: EndpointInfo,
        service_name: str,
        module_name: str,
        class_name: str,
        include_assert_calls: bool,
        asserts_methods: Set[str],
    ) -> None:
        """Add a test for a specific endpoint with function signatures.

        Args:
            lines: List to append test lines to
            entry: Endpoint information
            service_name: Name of the service
            module_name: Name of the module
            class_name: Name of the client class
            include_assert_calls: Whether to include assertion calls
            asserts_methods: Set of available assertion methods
        """
        endpoint = entry.endpoint
        if not endpoint:
            return

        http_info = f"{entry.http_method} {entry.path}".strip()
        skip_reason = f"Add tests for {service_name}.{module_name}.{entry.method_name} ({http_info})"

        lines.append(f'@pytest.mark.skip("{skip_reason}")')
        lines.append(f"def test_{entry.method_name}() -> None:")
        lines.append(f'    """Test {class_name}.{entry.method_name}: {entry.description}."""')

        # Generate method context for signature extraction
        method_context = MethodContext.from_endpoint(endpoint)

        # Add client instantiation example
        lines.append("")
        lines.append("    # Direct client usage:")
        lines.append(f"    client = {class_name}(base_client=...)")

        # Generate function signature
        all_params = method_context.required_params + method_context.optional_params
        param_str = ", ".join(all_params) if all_params else ""

        lines.append(f"    # Signature: client.{entry.method_name}({param_str}) -> {method_context.return_type}")

        # Add example call with placeholder values
        call_params = self._generate_example_params(method_context)
        lines.append(f"    # response = client.{entry.method_name}({call_params})")

        # Add facade usage example
        facade_attr = self._class_name_to_camel_case(class_name)
        lines.append("")
        lines.append("    # Facade usage:")
        lines.append(f"    # api_client = {self.facade_class_name}(base_client=...)")
        lines.append(f"    # response = api_client.{facade_attr}.{entry.method_name}({call_params})")

        # Add assertion call if available
        if include_assert_calls and entry.method_name in asserts_methods:
            lines.append("")
            lines.append("    # response = ...  # TODO: Implement actual call")
            lines.append(f"    # assert_{entry.method_name}(response)")
        else:
            lines.append("")
            lines.append("    # TODO: Implement test logic")

    def _add_placeholder_test(
        self,
        lines: List[str],
        entry: EndpointInfo,
        service_name: str,
        module_name: str,
        class_name: str,
    ) -> None:
        """Add a placeholder test for missing endpoint information.

        Args:
            lines: List to append test lines to
            entry: Endpoint information
            service_name: Name of the service
            module_name: Name of the module
            class_name: Name of the client class
        """
        skip_reason = f"Add tests for {service_name}.{module_name}.{entry.method_name}"

        lines.append(f'@pytest.mark.skip("{skip_reason}")')
        lines.append(f"def test_{entry.method_name}() -> None:")
        lines.append(f'    """Auto-generated placeholder for {class_name}.{entry.method_name}: {entry.description}."""')
        lines.append("    ...")

    def _generate_example_params(self, method_context: MethodContext) -> str:
        """Generate example parameter values for function calls.

        Args:
            method_context: Method context with parameter information

        Returns:
            String representation of example parameters
        """
        example_params = []

        # Process required parameters
        for param in method_context.required_params:
            param_name = param.split(":")[0].strip()
            if "id" in param_name.lower():
                example_params.append(f"{param_name}=1")
            elif param_name in ["payload", "data"]:
                example_params.append(f"{param_name}={{...}}")
            else:
                example_params.append(f'{param_name}="example"')

        # Add a few optional parameters as comments
        if method_context.optional_params:
            optional_examples = []
            for i, param in enumerate(method_context.optional_params[:2]):  # Limit to first 2
                param_name = param.split(":")[0].strip()
                if param_name == "params":
                    optional_examples.append(f"# {param_name}={{...}}")
                else:
                    optional_examples.append(f"# {param_name}=...")

            if optional_examples:
                if example_params:
                    example_params.extend(optional_examples)
                else:
                    example_params = optional_examples

        return ", ".join(example_params) if example_params else "..."

    def _class_name_to_camel_case(self, class_name: str) -> str:
        """Convert PascalCase class name to camelCase attribute name.

        Args:
            class_name: The class name to convert

        Returns:
            camelCase attribute name
        """
        if not class_name:
            return class_name
        return class_name[0].lower() + class_name[1:]
