"""Naming convention utilities for consistent code generation."""

import re


def to_snake_case(name: str) -> str:
    """Convert string to snake_case.

    Examples:
        'ApprovalProcessTemplate' -> 'approval_process_template'
        'HTTPValidationError' -> 'http_validation_error'
        'userID' -> 'user_id'
    """
    # Handle consecutive capitals (e.g., HTTPError -> HTTP_Error)
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)

    # Handle normal CamelCase (e.g., CamelCase -> Camel_Case)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)

    # Replace any remaining non-alphanumeric characters with underscores
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)

    # Remove multiple consecutive underscores
    name = re.sub(r'_+', '_', name)

    # Remove leading/trailing underscores
    name = name.strip('_')

    return name.lower()


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase (for class names).

    Examples:
        'approval_process_template' -> 'ApprovalProcessTemplate'
        'user-management' -> 'UserManagement'
        'http_validation_error' -> 'HttpValidationError'
    """
    # Replace non-alphanumeric characters with spaces
    name = re.sub(r'[^a-zA-Z0-9]', ' ', name)

    # Split by spaces and capitalize each word
    words = name.split()

    return ''.join(word.capitalize() for word in words if word)


def normalize_directory_name(name: str) -> str:
    """Normalize directory names to use underscores instead of hyphens.

    Examples:
        'role-groups' -> 'role_groups'
        'access-setting' -> 'access_setting'
        'element-documents' -> 'element_documents'
    """
    # Replace hyphens with underscores
    name = name.replace('-', '_')

    # Convert to snake_case for consistency
    return to_snake_case(name)


def normalize_file_name(class_name: str) -> str:
    """Convert class name to snake_case file name.

    Examples:
        'ApprovalProcessTemplateFilterRequest' -> 'approval_process_template_filter_request'
        'HTTPValidationError' -> 'http_validation_error'
    """
    return to_snake_case(class_name)


def normalize_module_name(name: str) -> str:
    """Normalize module names to be valid Python identifiers.

    Examples:
        'approval-processes' -> 'approval_processes'
        'model-rooms' -> 'model_rooms'
    """
    return normalize_directory_name(name)


def sanitize_inline_model_name(context: str) -> str:
    """Create a PascalCase model name from an arbitrary context string."""

    cleaned = context.replace("/", " ").replace("-", " ")
    cleaned = cleaned.replace("{", " ").replace("}", " ")
    cleaned = cleaned.replace(":", " ").replace(".", " ")
    cleaned = cleaned.replace("[", " ").replace("]", " ")
    cleaned = cleaned.replace("(", " ").replace(")", " ")
    cleaned = cleaned.replace("*", " ")

    return to_pascal_case(cleaned) or "InlineModel"
