import os
from typing import List, Dict
from jinja2 import Environment, PackageLoader


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

    env = Environment(
        loader=PackageLoader("my_codegen", "templates"),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_name)

    rendered = template.render(services=services)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)
