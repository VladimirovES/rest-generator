"""Enhanced client generator that creates models per endpoint."""

import os
from typing import List, Dict, Any
from pathlib import Path

from codegen.data_models import Endpoint, MethodContext
from codegen.client_generator import ClientGenerator
from dto_parser.model_generator import CustomModelGenerator
from utils.logger import logger
from utils.naming import normalize_directory_name


class EnhancedClientGenerator(ClientGenerator):
    """Extended client generator that creates models alongside endpoints."""

    def __init__(self, endpoints: List[Endpoint], imports: List[str], template_name: str, openapi_spec: Dict[str, Any]):
        super().__init__(endpoints, imports, template_name)
        self.openapi_spec = openapi_spec
        self.model_generator = None
        self.module_endpoints: Dict[str, List[Endpoint]] = {}

    def generate_clients_with_models(self, output_dir: str) -> Dict[str, str]:
        """Generate client files with models organized per endpoint.

        Args:
            output_dir: Base output directory for the service

        Returns:
            Dictionary mapping endpoint files to their class names
        """
        if not self.endpoints:
            logger.warning("No endpoints to generate")
            return {}

        # Initialize model generator
        self.model_generator = CustomModelGenerator(self.openapi_spec, output_dir)

        # Group endpoints by tag/file
        file_to_endpoints = self._group_endpoints_by_tag()
        file_to_class = {}

        for file_name, endpoints in file_to_endpoints.items():
            # Normalize directory name to use underscores instead of hyphens
            normalized_dir_name = normalize_directory_name(file_name)
            # Create module directory directly under service (no endpoints folder)
            module_dir = os.path.join(output_dir, normalized_dir_name)
            os.makedirs(module_dir, exist_ok=True)

            # Track endpoints associated with the module for auxiliary generators
            self.module_endpoints[normalized_dir_name] = endpoints

            # Generate models for all endpoints in this file
            all_model_names = set()
            for endpoint in endpoints:
                models = self.model_generator.generate_models_for_endpoint(
                    endpoint.path, endpoint.http_method, module_dir
                )
                all_model_names.update(models)

            # Ensure models package exports all collected models
            self.model_generator.finalize_models_package(
                os.path.join(module_dir, "models"), all_model_names
            )

            # Generate the client file
            class_name = self._tag_to_class_name(file_name)
            self._generate_module_client_file(module_dir, endpoints, class_name, all_model_names)

            # Generate __init__.py for the module package
            self._generate_module_init(module_dir, class_name)

            file_to_class[normalized_dir_name] = class_name

        # Generate main service __init__.py
        self._generate_service_init(output_dir, file_to_class)

        logger.info(f"Generated {len(file_to_class)} client files with models")
        return file_to_class

    def get_module_endpoints(self) -> Dict[str, List[Endpoint]]:
        """Return mapping of module names to their endpoints."""
        return self.module_endpoints

    def _generate_module_client_file(self, module_dir: str, endpoints: List[Endpoint], class_name: str, model_names: set) -> None:
        """Generate a client file for a module."""
        client_file = os.path.join(module_dir, "client.py")

        # Prepare template data
        template_data = {
            "class_name": class_name,
            "methods": endpoints,
            "imports": self._get_model_imports(model_names),
            "models_import_path": ".models"  # Relative import from models subdirectory
        }

        # Generate the file using the parent's template rendering
        content = self._render_template(template_data)

        with open(client_file, "w", encoding="utf-8") as f:
            f.write(content)

    def _get_model_imports(self, model_names: set) -> List[str]:
        """Get the list of model imports for the template."""
        if not model_names:
            return []

        # Return sorted list of model names for consistent imports
        return sorted(model_names)

    def _generate_module_init(self, module_dir: str, class_name: str) -> None:
        """Generate __init__.py for a module package."""
        init_file = os.path.join(module_dir, "__init__.py")

        content = f'''"""Generated module package: {class_name}."""

from .client import {class_name}

__all__ = ["{class_name}"]
'''

        with open(init_file, "w", encoding="utf-8") as f:
            f.write(content)

    def _generate_service_init(self, service_dir: str, file_to_class: Dict[str, str]) -> None:
        """Generate main __init__.py for the service package."""
        init_file = os.path.join(service_dir, "__init__.py")

        imports = []
        all_exports = []

        for module_name, class_name in file_to_class.items():
            imports.append(f"from .{module_name} import {class_name}")
            all_exports.append(class_name)

        content = '"""Generated service clients."""\n\n'
        content += '\n'.join(imports)
        content += f'\n\n__all__ = [\n'
        for export in sorted(all_exports):
            content += f'    "{export}",\n'
        content += ']\n'

        with open(init_file, "w", encoding="utf-8") as f:
            f.write(content)

    def _render_template(self, template_data: Dict[str, Any]) -> str:
        """Render the client template with the given data."""
        # Convert endpoints to method contexts
        if 'methods' in template_data and template_data['methods'] and isinstance(template_data['methods'][0], Endpoint):
            template_data['methods'] = [MethodContext.from_endpoint(ep) for ep in template_data['methods']]

        return self.template.render(**template_data)
