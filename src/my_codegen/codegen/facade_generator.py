import os
from typing import Dict
from jinja2 import Environment, FileSystemLoader


class FacadeGenerator:
    def __init__(self, facade_class_name: str, template_path: str):
        self.facade_class_name = facade_class_name
        self.template_path = template_path
        self.env = Environment(loader=FileSystemLoader(''), trim_blocks=True, lstrip_blocks=True)
        self.template = self.env.get_template(self.template_path)

    def generate_facade(self,
                        file_to_class: Dict[str, str],
                        output_dir: str,
                        file_name: str) -> None:
        client_files = sorted([f for f in file_to_class if f.endswith("_client.py")])
        imports_data = []
        for fname in client_files:
            module_name = fname[:-3]
            class_name = file_to_class[fname]
            attribute_name = class_name.lower()
            imports_data.append({
                "module_name": module_name,
                "class_name": class_name,
                "attribute_name": attribute_name,
            })

        rendered = self.template.render(
            facade_class_name=self.facade_class_name,
            imports=imports_data,
            docstring_indent="    "
        )
        facade_path = os.path.join(output_dir, file_name)
        with open(facade_path, "w", encoding="utf-8") as f:
            f.write(rendered)
