"""Custom model generator that creates Pydantic models from parsed schemas."""

import os
from typing import Dict, Set, List
from pathlib import Path

from my_codegen.dto_parser.schema_parser import SchemaParser, ModelDefinition
from my_codegen.utils.naming import normalize_file_name


class CustomModelGenerator:
    """Generates Pydantic model files from parsed OpenAPI schemas."""

    def __init__(self, openapi_spec: Dict, output_base_dir: str):
        self.parser = SchemaParser(openapi_spec)
        self.output_base_dir = output_base_dir
        self.all_models = {}

    def generate_models_for_endpoint(self, endpoint_path: str, method: str, endpoint_dir: str) -> List[str]:
        """Generate models for a specific endpoint and save them in the endpoint's models directory.

        Args:
            endpoint_path: The API path (e.g., '/users/{id}')
            method: HTTP method (e.g., 'GET')
            endpoint_dir: Directory where endpoint files are stored

        Returns:
            List of generated model class names
        """
        # Parse all schemas if not already done
        if not self.all_models:
            self.all_models = self.parser.parse_all_schemas()

        # Get models used by this endpoint
        endpoint_models = self.parser.get_models_for_endpoint(endpoint_path, method)

        if not endpoint_models:
            return []

        # Create models directory for this endpoint
        models_dir = os.path.join(endpoint_dir, "models")
        os.makedirs(models_dir, exist_ok=True)

        # Generate __init__.py for models
        self._generate_models_init(models_dir, endpoint_models)

        # Generate individual model files
        generated_classes = []
        for model_name in endpoint_models:
            if model_name in self.all_models:
                model_def = self.all_models[model_name]
                self._generate_model_file(models_dir, model_def)
                generated_classes.append(model_name)

        return generated_classes

    def _generate_models_init(self, models_dir: str, model_names: Set[str]) -> None:
        """Generate __init__.py file for the models package."""
        init_path = os.path.join(models_dir, "__init__.py")

        imports = []
        all_exports = []

        for model_name in sorted(model_names):
            if model_name in self.all_models:
                file_name = normalize_file_name(model_name)
                imports.append(f"from .{file_name} import {model_name}")
                all_exports.append(model_name)

        content = '"""Generated models for this endpoint."""\n\n'
        content += '\n'.join(imports)
        content += f'\n\n__all__ = [\n'
        for export in all_exports:
            content += f'    "{export}",\n'
        content += ']\n'

        with open(init_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _generate_model_file(self, models_dir: str, model_def: ModelDefinition) -> None:
        """Generate a single model file."""
        file_name = normalize_file_name(model_def.name)
        file_path = os.path.join(models_dir, f"{file_name}.py")

        content = self._generate_model_content(model_def)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _generate_model_content(self, model_def: ModelDefinition) -> str:
        """Generate the content for a model file."""
        lines = []

        # Add file docstring
        lines.append(f'"""Generated model: {model_def.name}."""')
        lines.append("")

        # Add imports
        imports = self._get_imports_for_model(model_def)
        lines.extend(imports)
        if imports:
            lines.append("")

        # Generate model class
        if model_def.is_enum:
            lines.extend(self._generate_enum_class(model_def))
        elif model_def.base_type.startswith("TypeAlias"):
            lines.extend(self._generate_type_alias(model_def))
        else:
            lines.extend(self._generate_pydantic_class(model_def))

        return "\n".join(lines)

    def _get_imports_for_model(self, model_def: ModelDefinition) -> List[str]:
        """Get all necessary imports for a model."""
        imports = []

        # Add Pydantic imports
        if model_def.is_enum:
            if model_def.base_type == "Enum":
                imports.append("from enum import Enum")
            else:
                imports.append("from enum import IntEnum")
        elif not model_def.base_type.startswith("TypeAlias"):
            imports.append("from pydantic import BaseModel")

            # Add field imports if needed
            has_constraints = any(field.constraints for field in model_def.fields)
            if has_constraints:
                imports.append("from pydantic import Field")

        # Add type resolver imports from the stored imports
        if model_def.imports:
            # Temporarily set imports to use the type resolver's import formatting
            self.parser.type_resolver.imports = model_def.imports.copy()
            imports.extend(self.parser.type_resolver.get_imports())

        return imports

    def _generate_enum_class(self, model_def: ModelDefinition) -> List[str]:
        """Generate enum class definition."""
        lines = []

        if model_def.description:
            lines.append(f'class {model_def.name}({model_def.base_type}):')
            lines.append(f'    """{model_def.description}"""')
        else:
            lines.append(f'class {model_def.name}({model_def.base_type}):')

        if model_def.enum_values:
            for i, value in enumerate(model_def.enum_values):
                if isinstance(value, str):
                    lines.append(f'    VALUE_{i+1} = "{value}"')
                else:
                    lines.append(f'    VALUE_{i+1} = {value}')
        else:
            lines.append("    pass")

        return lines

    def _generate_type_alias(self, model_def: ModelDefinition) -> List[str]:
        """Generate type alias definition."""
        lines = []

        if model_def.description:
            lines.append(f'"""{model_def.description}"""')

        lines.append(f'{model_def.name} = {model_def.base_type.replace("TypeAlias = ", "")}')

        return lines

    def _generate_pydantic_class(self, model_def: ModelDefinition) -> List[str]:
        """Generate Pydantic BaseModel class definition."""
        lines = []

        # Class definition
        if model_def.description:
            lines.append(f'class {model_def.name}({model_def.base_type}):')
            lines.append(f'    """{model_def.description}"""')
        else:
            lines.append(f'class {model_def.name}({model_def.base_type}):')

        # Fields
        if not model_def.fields:
            lines.append("    pass")
        else:
            for field in model_def.fields:
                field_lines = self._generate_field_definition(field)
                lines.extend(field_lines)

        return lines

    def _generate_field_definition(self, field) -> List[str]:
        """Generate field definition lines."""
        lines = []

        # Build field definition
        if field.required and field.default is None:
            if field.constraints:
                constraint_args = self._build_field_constraints(field.constraints)
                field_def = f"{field.name}: {field.type_str} = Field({constraint_args})"
            else:
                field_def = f"{field.name}: {field.type_str}"
        else:
            if field.constraints:
                constraint_args = self._build_field_constraints(field.constraints)
                if field.default:
                    field_def = f"{field.name}: {field.type_str} = Field(default={field.default}, {constraint_args})"
                else:
                    field_def = f"{field.name}: {field.type_str} = Field({constraint_args})"
            else:
                field_def = f"{field.name}: {field.type_str} = {field.default or 'None'}"

        lines.append(f"    {field_def}")

        # Add field description as comment if present
        if field.description:
            lines.append(f'    """{field.description}"""')

        return lines

    def _build_field_constraints(self, constraints: Dict) -> str:
        """Build Field constraint arguments."""
        constraint_parts = []

        constraint_mapping = {
            "minLength": "min_length",
            "maxLength": "max_length",
            "minimum": "ge",
            "maximum": "le",
            "pattern": "regex"
        }

        for openapi_name, pydantic_name in constraint_mapping.items():
            if openapi_name in constraints:
                value = constraints[openapi_name]
                if openapi_name == "pattern":
                    constraint_parts.append(f'{pydantic_name}=r"{value}"')
                else:
                    constraint_parts.append(f"{pydantic_name}={value}")

        return ", ".join(constraint_parts)