import os
from typing import Dict, List
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
from utils.naming import to_snake_case


@dataclass
class ClientImport:
    module_name: str
    class_name: str
    attribute_name: str


class FacadeGenerator:
    def __init__(self, facade_class_name: str, template_name: str):
        self.facade_class_name = facade_class_name
        self.template_name = template_name
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, "templates")
        templates_path = os.path.abspath(templates_dir)

        self.env = Environment(
            loader=FileSystemLoader(templates_path),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.template = self.env.get_template(self.template_name)

    def generate_facade(
        self, file_to_class: Dict[str, str], output_dir: str, file_name: str
    ) -> None:
        imports_data = self._prepare_imports_data(file_to_class)

        rendered = self.template.render(
            facade_class_name=self.facade_class_name,
            imports=imports_data,
            docstring_indent=" ",
        )

        facade_path = os.path.join(output_dir, file_name)
        with open(facade_path, "w", encoding="utf-8") as f:
            f.write(rendered)

    def _prepare_imports_data(
        self, file_to_class: Dict[str, str]
    ) -> List[ClientImport]:
        """Prepare client import data for facade generation"""
        imports_data = []

        for module_name, class_name in sorted(file_to_class.items()):
            attribute_name = self._class_name_to_snake_case(class_name)

            imports_data.append(
                ClientImport(
                    module_name=module_name,
                    class_name=class_name,
                    attribute_name=attribute_name,
                )
            )

        return imports_data

    def _class_name_to_snake_case(self, class_name: str) -> str:
        """Convert PascalCase class name to snake_case attribute name

        Examples:
            'MaintenanceProvider' -> 'maintenance_provider'
            'LaborCostsCatalog' -> 'labor_costs_catalog'
            'TechnicalSupportRequests' -> 'technical_support_requests'
        """
        return to_snake_case(class_name)
