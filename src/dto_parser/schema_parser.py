"""OpenAPI schema parser for extracting model definitions."""

from typing import Dict, Any, List, Set, Optional
import json
import re
from dataclasses import dataclass

from dto_parser.type_resolver import TypeResolver
from utils.naming import to_pascal_case


@dataclass
class ModelField:
    """Represents a field in a Pydantic model."""
    name: str
    type_str: str
    required: bool = True
    default: Optional[str] = None
    description: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = None


@dataclass
class ModelDefinition:
    """Represents a complete model definition."""
    name: str
    fields: List[ModelField]
    description: Optional[str] = None
    is_enum: bool = False
    enum_values: Optional[List[Any]] = None
    base_type: str = "BaseConfigModel"
    imports: Optional[Set[str]] = None


class SchemaParser:
    """Parses OpenAPI schemas and extracts model definitions."""

    def __init__(self, openapi_spec: Dict[str, Any]):
        self.spec = openapi_spec
        self.type_resolver = TypeResolver()
        self.name_mapping: Dict[str, str] = {}
        self.used_model_names: Set[str] = set()
        self.type_resolver.set_ref_name_transform(self._get_or_create_model_name)
        self.parsed_models: Dict[str, ModelDefinition] = {}
        self.endpoint_models: Dict[str, Set[str]] = {}  # endpoint -> model names

    def parse_all_schemas(self) -> Dict[str, ModelDefinition]:
        """Parse all schema definitions from the OpenAPI spec."""
        components = self.spec.get("components", {})
        schemas = components.get("schemas", {})

        for schema_name, schema_def in schemas.items():
            model = self._parse_schema_definition(schema_name, schema_def)
            self.parsed_models[model.name] = model

        return self.parsed_models

    def get_models_for_endpoint(self, path: str, method: str) -> Set[str]:
        """Get all models used by a specific endpoint."""
        endpoint_key = f"{method.upper()}:{path}"

        if endpoint_key not in self.endpoint_models:
            self.endpoint_models[endpoint_key] = self._extract_endpoint_models(path, method)

        return self.endpoint_models[endpoint_key]

    def _extract_endpoint_models(self, path: str, method: str) -> Set[str]:
        """Extract all models referenced by a specific endpoint."""
        models = set()

        # Get the operation from the spec
        paths = self.spec.get("paths", {})
        path_item = paths.get(path, {})
        operation = path_item.get(method.lower(), {})

        if not operation:
            return models

        # Check parameters
        parameters = operation.get("parameters", [])
        for param in parameters:
            if "schema" in param:
                models.update(self._extract_models_from_schema(param["schema"]))

        # Check request body
        request_body = operation.get("requestBody", {})
        if request_body:
            content = request_body.get("content", {})
            for media_type, media_content in content.items():
                if "schema" in media_content:
                    models.update(self._extract_models_from_schema(media_content["schema"]))

        # Check responses
        responses = operation.get("responses", {})
        for status_code, response in responses.items():
            content = response.get("content", {})
            for media_type, media_content in content.items():
                if "schema" in media_content:
                    models.update(self._extract_models_from_schema(media_content["schema"]))

        return models

    def _get_or_create_model_name(self, original_name: str) -> str:
        """Normalize schema names to valid Python class identifiers."""
        if original_name in self.name_mapping:
            return self.name_mapping[original_name]

        # First, handle special patterns
        cleaned = original_name

        # Replace common separators with spaces
        cleaned = cleaned.replace("_", " ").replace("-", " ").replace(".", " ")

        # Handle CamelCase by adding spaces before capitals
        cleaned = re.sub(r'([a-z])([A-Z])', r'\1 \2', cleaned)

        # Handle acronyms (e.g., HTTPValidationError -> HTTP Validation Error)
        cleaned = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1 \2', cleaned)

        # Remove any non-alphanumeric characters and replace with spaces
        cleaned = re.sub(r'[^a-zA-Z0-9]+', ' ', cleaned)

        # Remove extra spaces and convert to PascalCase
        sanitized = to_pascal_case(cleaned)

        if not sanitized:
            sanitized = to_pascal_case(original_name)
        if not sanitized:
            sanitized = f"Model{len(self.name_mapping) + 1}"

        candidate = sanitized
        suffix = 1
        while candidate in self.used_model_names:
            suffix += 1
            candidate = f"{sanitized}{suffix}"

        self.used_model_names.add(candidate)
        self.name_mapping[original_name] = candidate
        return candidate

    def _extract_models_from_schema(self, schema: Dict[str, Any]) -> Set[str]:
        """Recursively extract all model references from a schema."""
        models = set()

        if "$ref" in schema:
            ref_name = schema["$ref"].split("/")[-1]
            models.add(self._get_or_create_model_name(ref_name))
            return models

        if "allOf" in schema:
            for sub_schema in schema["allOf"]:
                models.update(self._extract_models_from_schema(sub_schema))

        if "oneOf" in schema:
            for sub_schema in schema["oneOf"]:
                models.update(self._extract_models_from_schema(sub_schema))

        if "anyOf" in schema:
            for sub_schema in schema["anyOf"]:
                models.update(self._extract_models_from_schema(sub_schema))

        if schema.get("type") == "array" and "items" in schema:
            models.update(self._extract_models_from_schema(schema["items"]))

        if schema.get("type") == "object" and "properties" in schema:
            for prop_schema in schema["properties"].values():
                models.update(self._extract_models_from_schema(prop_schema))

        return models

    def _parse_schema_definition(self, original_name: str, schema: Dict[str, Any]) -> ModelDefinition:
        """Parse a single schema definition into a ModelDefinition."""

        model_name = self._get_or_create_model_name(original_name)

        # Handle enums
        if "enum" in schema:
            return ModelDefinition(
                name=model_name,
                fields=[],
                description=schema.get("description"),
                is_enum=True,
                enum_values=schema["enum"],
                base_type="Enum" if self._is_string_enum(schema["enum"]) else "IntEnum"
            )

        # Handle object types
        if schema.get("type") == "object" or "properties" in schema:
            return self._parse_object_schema(schema, model_name)

        # Handle simple types (create type alias)
        type_str = self.type_resolver.resolve_type(schema, model_name)
        return ModelDefinition(
            name=model_name,
            fields=[],
            description=schema.get("description"),
            base_type=f"TypeAlias = {type_str}"
        )

    def _parse_object_schema(self, schema: Dict[str, Any], model_name: str) -> ModelDefinition:
        """Parse an object schema into a ModelDefinition."""
        properties = schema.get("properties", {})
        required_fields = set(schema.get("required", []))

        # Clear imports and collect during field parsing
        self.type_resolver.imports.clear()

        fields = []
        for field_name, field_schema in properties.items():
            field = self._parse_field(field_name, field_schema, field_name in required_fields)
            fields.append(field)

        # Capture imports for this model
        model_imports = self.type_resolver.imports.copy()

        return ModelDefinition(
            name=model_name,
            fields=fields,
            description=schema.get("description"),
            base_type="BaseConfigModel",
            imports=model_imports
        )

    def _parse_field(self, name: str, schema: Dict[str, Any], required: bool) -> ModelField:
        """Parse a field schema into a ModelField."""
        type_str = self.type_resolver.resolve_type(schema, name)

        # Handle default values
        default = None
        if not required:
            if "default" in schema:
                default_value = schema["default"]
                if isinstance(default_value, str):
                    default = f'"{default_value}"'
                elif default_value is None:
                    default = "None"
                else:
                    default = str(default_value)
            else:
                default = "None"
                if not type_str.startswith("Optional["):
                    type_str = f"Optional[{type_str}]"
                    self.type_resolver.imports.add("Optional")

        # Extract constraints
        constraints = {}
        for constraint in ["minLength", "maxLength", "minimum", "maximum", "pattern"]:
            if constraint in schema:
                constraints[constraint] = schema[constraint]

        return ModelField(
            name=name,
            type_str=type_str,
            required=required,
            default=default,
            description=schema.get("description"),
            constraints=constraints if constraints else None
        )

    def _is_string_enum(self, values: List[Any]) -> bool:
        """Check if enum values are all strings."""
        return all(isinstance(v, str) for v in values)
