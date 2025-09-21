import os
from typing import List, Dict
from jinja2 import Environment, FileSystemLoader


def find_services_with_facade(base_dir: str = "http_clients") -> List[Dict[str, str]]:
    services_info = []
    for item in os.listdir(base_dir):
        service_path = os.path.join(base_dir, item)
        if os.path.isdir(service_path):
            facade_file = os.path.join(service_path, "facade.py")
            if os.path.exists(facade_file):
                api_class = (
                    "".join(word.capitalize() for word in item.split("_")) + "Facade"
                )
                services_info.append({"service_name": item, "api_class": api_class})
    return services_info


def generate_app_facade(
    template_name: str,
    output_path: str = "api_facade.py",
    base_dir: str = "http_clients",
) -> None:
    services = find_services_with_facade(base_dir)

    # Get absolute path to templates directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(current_dir, "..", "templates")
    templates_path = os.path.abspath(templates_dir)

    env = Environment(
        loader=FileSystemLoader(templates_path),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_name)

    rendered = template.render(services=services)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
