"""Custom model generator that creates Pydantic models from parsed schemas."""

import os
import re
from typing import Dict, Iterable, List, Set

from dto_parser.schema_parser import SchemaParser, ModelDefinition
from utils.naming import normalize_file_name


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

        # Generate BaseConfigModel file for this service
        self._generate_base_config(models_dir)

        # Resolve complete set of models including dependencies
        models_to_generate = self._resolve_model_dependencies(endpoint_models)

        # Generate individual model files and track the classes we actually create
        generated_classes: List[str] = []
        for model_name in sorted(models_to_generate):
            if self._should_skip_model(model_name):
                continue

            if model_name in self.all_models:
                model_def = self.all_models[model_name]
                self._generate_model_file(models_dir, model_def)
                generated_classes.append(model_name)

        return generated_classes

    def _generate_base_config(self, models_dir: str) -> None:
        """Generate base_config.py file with BaseConfigModel."""
        base_config_path = os.path.join(models_dir, "base_config.py")

        # Only generate if it doesn't exist to avoid overwriting
        if os.path.exists(base_config_path):
            return

        content = '''"""Base configuration for Pydantic models."""

from pydantic import BaseModel


class BaseConfigModel(BaseModel):
    """Base model class with common configuration."""

    class Config:
        extra = "forbid"
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True
'''

        with open(base_config_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _generate_models_init(self, models_dir: str, model_names: Iterable[str]) -> None:
        """Generate __init__.py file for the models package."""
        # Ensure the models directory exists
        os.makedirs(models_dir, exist_ok=True)
        init_path = os.path.join(models_dir, "__init__.py")

        imports = []
        all_exports = []

        for model_name in sorted(set(model_names)):
            # Skip http_validation_error models
            if self._should_skip_model(model_name):
                continue

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

    def finalize_models_package(self, models_dir: str, model_names: Iterable[str]) -> None:
        """Create or update models package initializer with collected models."""
        self._generate_models_init(models_dir, model_names)

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
            imports.append("from .base_config import BaseConfigModel")

            # Add field imports if needed
            has_constraints = any(field.constraints for field in model_def.fields)
            if has_constraints:
                imports.append("from pydantic import Field")

        # Add type resolver imports from the stored imports
        if model_def.imports:
            # Temporarily set imports to use the type resolver's import formatting
            self.parser.type_resolver.imports = model_def.imports.copy()
            imports.extend(self.parser.type_resolver.get_imports())

        # Add local model imports for models referenced in this model
        local_model_imports = self._get_local_model_imports(model_def)
        imports.extend(local_model_imports)

        return imports

    def _resolve_model_dependencies(self, model_names: Iterable[str]) -> Set[str]:
        """Expand the set of models to include their dependent models."""
        resolved: Set[str] = set()
        stack = list(model_names)

        while stack:
            model_name = stack.pop()
            if model_name in resolved or self._should_skip_model(model_name):
                continue

            resolved.add(model_name)

            if model_name not in self.all_models:
                continue

            model_def = self.all_models[model_name]
            for dependency in self._extract_referenced_models(model_def):
                if dependency not in resolved:
                    stack.append(dependency)

        return resolved

    @staticmethod
    def _should_skip_model(model_name: str) -> bool:
        lowered = model_name.lower()
        return lowered in {"httpvalidationerror", "http_validation_error"}

    def _extract_referenced_models(self, model_def: ModelDefinition) -> Set[str]:
        """Find other models referenced within the provided model definition."""
        referenced_models: Set[str] = set()

        def _scan_text(value: str) -> None:
            for candidate in re.findall(r"\b[A-Z][a-zA-Z0-9_]*\b", value):
                if candidate in {"List", "Dict", "Optional", "Union", "Set", "Tuple", "UUID", "datetime", "date", "time", "Any", "BaseModel", "BaseConfigModel"}:
                    continue
                if candidate == model_def.name:
                    continue
                if candidate in self.all_models and not self._should_skip_model(candidate):
                    referenced_models.add(candidate)

        for field in model_def.fields:
            _scan_text(field.type_str)

        if model_def.base_type:
            _scan_text(model_def.base_type)

        return referenced_models

    def _get_local_model_imports(self, model_def: ModelDefinition) -> List[str]:
        """Get imports for other models referenced in this model."""
        imports = []

        referenced_models = self._extract_referenced_models(model_def)

        if referenced_models:
            for model in sorted(referenced_models):
                file_name = normalize_file_name(model)
                imports.append(f"from .{file_name} import {model}")

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
                field_lines = self._generate_field_definition(field, model_def.name)
                lines.extend(field_lines)

        return lines

    def _generate_field_definition(self, field, current_class_name: str = "") -> List[str]:
        """Generate field definition lines."""
        lines = []

        # Handle self-references by wrapping in quotes
        type_str = self._handle_self_reference(field.type_str, current_class_name)

        # Build field definition
        if field.required and field.default is None:
            if field.constraints:
                constraint_args = self._build_field_constraints(field.constraints)
                field_def = f"{field.name}: {type_str} = Field({constraint_args})"
            else:
                field_def = f"{field.name}: {type_str}"
        else:
            if field.constraints:
                constraint_args = self._build_field_constraints(field.constraints)
                if field.default:
                    field_def = f"{field.name}: {type_str} = Field(default={field.default}, {constraint_args})"
                else:
                    field_def = f"{field.name}: {type_str} = Field({constraint_args})"
            else:
                field_def = f"{field.name}: {type_str} = {field.default or 'None'}"

        lines.append(f"    {field_def}")

        # Add field description as comment if present
        if field.description:
            lines.append(f'    """{field.description}"""')

        return lines

    def _handle_self_reference(self, type_str: str, current_class_name: str) -> str:
        """Handle self-references by wrapping class names in quotes."""
        if not current_class_name:
            return type_str

        # Pattern to find self-references in type annotations
        # Matches patterns like List[ClassName], Optional[ClassName], Union[ClassName, Other], etc.
        import re
        pattern = rf'\b{re.escape(current_class_name)}\b'

        # Replace self-references with quoted versions
        result = re.sub(pattern, f'"{current_class_name}"', type_str)
        return result

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
