"""Utilities for generating placeholder test structure."""

import os
from typing import Dict


class TestsGenerator:
    """Generate skeletal test folders mirroring service clients."""

    def __init__(self, base_dir: str) -> None:
        self.base_dir = base_dir

    def generate(self, service_name: str, file_to_class: Dict[str, str]) -> None:
        """Create directories and placeholder tests for a service."""
        if not file_to_class:
            return

        service_dir = os.path.join(self.base_dir, service_name)
        os.makedirs(service_dir, exist_ok=True)

        self._ensure_init(self.base_dir)
        self._ensure_init(service_dir)

        for module_name in sorted(file_to_class):
            class_name = file_to_class[module_name]
            module_dir = os.path.join(service_dir, module_name)
            os.makedirs(module_dir, exist_ok=True)
            self._ensure_init(module_dir)
            self._create_placeholder_test(module_dir, service_name, module_name, class_name)

    def _ensure_init(self, directory: str) -> None:
        init_file = os.path.join(directory, "__init__.py")
        if os.path.exists(init_file):
            return
        with open(init_file, "w", encoding="utf-8") as f:
            f.write('"""Package marker."""\n')

    def _create_placeholder_test(
        self, module_dir: str, service_name: str, module_name: str, class_name: str
    ) -> None:
        test_file = os.path.join(module_dir, f"test_{module_name}.py")
        if os.path.exists(test_file):
            return

        content = f'''"""Placeholder tests for {class_name}."""

import pytest


@pytest.mark.skip("Add meaningful tests for {service_name}.{module_name}")
def test_{module_name}_placeholder() -> None:
    """Auto-generated placeholder test for {class_name}."""

'''

        with open(test_file, "w", encoding="utf-8") as f:
            f.write(content)
