"""Naming convention utilities for consistent code generation."""

import re


def to_snake_case(name: str) -> str:
    """Convert string to snake_case.

    Examples:
        'ApprovalProcessTemplate' -> 'approval_process_template'
        'HTTPValidationError' -> 'http_validation_error'
        'userID' -> 'user_id'
    """
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)

    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)

    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)

    name = re.sub(r"_+", "_", name)

    name = name.strip("_")

    return name.lower()


def to_pascal_case(name: str) -> str:
    """Convert string to PascalCase (for class names).

    Examples:
        'approval_process_template' -> 'ApprovalProcessTemplate'
        'user-management' -> 'UserManagement'
        'http_validation_error' -> 'HttpValidationError'
        'labor_costs_catalog' -> 'LaborCostsCatalog'
        'catalog_nomenclatures' -> 'CatalogNomenclatures'
        'technical_support_requests' -> 'TechnicalSupportRequests'
        'ReclamationActs' -> 'ReclamationActs' (already PascalCase, preserve it)
        'WarrantyTypes' -> 'WarrantyTypes' (already PascalCase, preserve it)
    """
    has_separators = bool(re.search(r"[^a-zA-Z0-9]", name))
    if (
        not has_separators
        and name
        and name[0].isupper()
        and any(c.islower() for c in name)
        and any(c.isupper() for c in name[1:])
    ):
        return name

    name = re.sub(r"[^a-zA-Z0-9]", " ", name)

    words = name.split()

    return "".join(word.capitalize() for word in words if word)


def normalize_directory_name(name: str) -> str:
    """Normalize directory names to use underscores instead of hyphens.

    Examples:
        'role-groups' -> 'role_groups'
        'access-setting' -> 'access_setting'
        'element-documents' -> 'element_documents'
    """
    name = name.replace("-", "_")

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
