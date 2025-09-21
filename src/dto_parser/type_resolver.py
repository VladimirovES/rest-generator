"""Type resolution utilities for OpenAPI schemas."""

from typing import Any, Callable, Dict, List, Optional, Set, Union
import re


class TypeResolver:
    """Resolves OpenAPI types to Python/Pydantic types."""

    BASIC_TYPE_MAPPING = {
        "string": "str",
        "integer": "int",
        "number": "float",
        "boolean": "bool",
        "array": "List",
        "object": "Dict[str, Any]",
    }

    FORMAT_MAPPING = {
        "date": "date",
        "date-time": "datetime",
        "email": "EmailStr",
        "uuid": "UUID",
        "uri": "AnyUrl",
        "binary": "bytes",
    }

    def __init__(self):
        self.imports: Set[str] = set()
        self.model_references: Set[str] = set()
        self.ref_name_transform: Optional[Callable[[str], str]] = None

    def set_ref_name_transform(self, transform: Callable[[str], str]) -> None:
        """Register a transformer applied to $ref targets before usage."""
        self.ref_name_transform = transform

    def resolve_type(self, schema: Dict[str, Any], name_hint: str = "") -> str:
        """Resolve OpenAPI schema to Python type string.

        Args:
            schema: OpenAPI schema definition
            name_hint: Hint for naming complex types

        Returns:
            Python type string
        """
        if not schema:
            self.imports.add("Any")
            return "Any"

        # Handle $ref
        if "$ref" in schema:
            ref_name = self._extract_ref_name(schema["$ref"])
            if self.ref_name_transform:
                ref_name = self.ref_name_transform(ref_name)
            self.model_references.add(ref_name)
            return ref_name

        # Handle allOf, oneOf, anyOf
        if "allOf" in schema:
            return self._handle_composition(schema["allOf"], "Union", name_hint)
        if "oneOf" in schema:
            return self._handle_composition(schema["oneOf"], "Union", name_hint)
        if "anyOf" in schema:
            return self._handle_composition(schema["anyOf"], "Union", name_hint)

        # Handle arrays
        if schema.get("type") == "array":
            items = schema.get("items", {})
            item_type = self.resolve_type(items, f"{name_hint}Item")
            self.imports.add("List")
            return f"List[{item_type}]"

        # Handle objects
        if schema.get("type") == "object":
            return self._handle_object_type(schema, name_hint)

        # Handle enums
        if "enum" in schema:
            return self._handle_enum(schema, name_hint)

        # Handle basic types with format
        schema_type = schema.get("type", "string")
        schema_format = schema.get("format")

        if schema_format and schema_format in self.FORMAT_MAPPING:
            type_name = self.FORMAT_MAPPING[schema_format]
            self._add_import_for_type(type_name)
            return type_name

        # Handle nullable types
        basic_type = self.BASIC_TYPE_MAPPING.get(schema_type, "Any")
        if basic_type == "List":
            self.imports.add("List")
        elif basic_type == "Dict[str, Any]":
            self.imports.add("Dict")
            self.imports.add("Any")
        elif basic_type == "Any":
            self.imports.add("Any")

        if schema.get("nullable", False):
            self.imports.add("Optional")
            return f"Optional[{basic_type}]"

        return basic_type

    def _extract_ref_name(self, ref: str) -> str:
        """Extract model name from $ref."""
        return ref.split("/")[-1]

    def _handle_composition(self, schemas: List[Dict], composition_type: str, name_hint: str) -> str:
        """Handle allOf, oneOf, anyOf."""
        if not schemas:
            self.imports.add("Any")
            return "Any"

        resolved_types = []
        for schema in schemas:
            resolved_type = self.resolve_type(schema, name_hint)
            resolved_types.append(resolved_type)

        if len(resolved_types) == 1:
            single_type = resolved_types[0]
            if single_type == "Any":
                self.imports.add("Any")
            return single_type

        self.imports.add("Union")
        if any(resolved_type == "Any" for resolved_type in resolved_types):
            self.imports.add("Any")
        return f"Union[{', '.join(resolved_types)}]"

    def _handle_object_type(self, schema: Dict[str, Any], name_hint: str) -> str:
        """Handle object types."""
        properties = schema.get("properties", {})

        if not properties:
            # Generic object
            self.imports.add("Dict")
            self.imports.add("Any")
            return "Dict[str, Any]"

        # If it has properties, it should be a separate model
        if name_hint:
            model_name = self._format_class_name(name_hint)
            self.model_references.add(model_name)
            return model_name

        self.imports.add("Dict")
        self.imports.add("Any")
        return "Dict[str, Any]"

    def _handle_enum(self, schema: Dict[str, Any], name_hint: str) -> str:
        """Handle enum types."""
        enum_values = schema["enum"]
        if not enum_values:
            return "str"

        # Determine enum type based on values
        if all(isinstance(v, str) for v in enum_values):
            base_type = "str"
        elif all(isinstance(v, int) for v in enum_values):
            base_type = "int"
        else:
            base_type = "Any"
            self.imports.add("Any")

        if name_hint:
            enum_name = self._format_class_name(f"{name_hint}Enum")
            self.model_references.add(enum_name)
            return enum_name

        if base_type == "Any":
            self.imports.add("Any")
        return base_type

    def _add_import_for_type(self, type_name: str) -> None:
        """Add necessary imports for special types."""
        type_imports = {
            "date": "date",
            "datetime": "datetime",
            "EmailStr": "EmailStr",
            "UUID": "UUID",
            "AnyUrl": "AnyUrl",
        }

        if type_name in type_imports:
            self.imports.add(type_name)

    def _format_class_name(self, name: str) -> str:
        """Format string as a proper Python class name."""
        from utils.naming import to_pascal_case
        return to_pascal_case(name) or "Model"

    def get_imports(self) -> List[str]:
        """Get all required imports."""
        import_lines = []

        # Standard library imports
        std_imports = []
        if "date" in self.imports:
            std_imports.append("date")
        if "datetime" in self.imports:
            std_imports.append("datetime")
        if "UUID" in self.imports:
            std_imports.append("UUID")

        if std_imports:
            datetime_imports = [i for i in std_imports if i in ["date", "datetime"]]
            if datetime_imports:
                import_lines.append(f"from datetime import {', '.join(datetime_imports)}")
            if "UUID" in std_imports:
                import_lines.append("from uuid import UUID")

        # Typing imports
        typing_imports = [imp for imp in self.imports if imp in ["List", "Dict", "Any", "Optional", "Union"]]
        if typing_imports:
            import_lines.append(f"from typing import {', '.join(sorted(typing_imports))}")

        # Pydantic imports
        pydantic_imports = [imp for imp in self.imports if imp in ["EmailStr", "AnyUrl"]]
        if pydantic_imports:
            import_lines.append(f"from pydantic import {', '.join(sorted(pydantic_imports))}")

        return import_lines
