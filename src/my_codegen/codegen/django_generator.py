import re
from pathlib import Path
from typing import Any, Dict, List
from jinja2 import Template

def make_folder_name(title: str) -> str:
    name = title.lower().strip()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^\w_]", "", name)
    return name

def generate_django_code(swagger_dict: Dict[str, Any], base_output_dir: str) -> None:
    """
    Генерирует Django-подобный клиент (эндпоинты, фасад) и модели Pydantic
    в указанный каталог base_output_dir.

    :param swagger_dict: Парсенный swagger (dict из JSON).
    :param base_output_dir: Путь к папке, куда будем складывать файлы (обычно http_clients/<service_name>).
    """

    info = swagger_dict.get("info", {})
    module_title = info.get("title", "module")
    MODULE_FOLDER = make_folder_name(module_title)

    BASE_OUTPUT_DIR = Path(base_output_dir)  # <= "http_clients/<service_name>"
    BASE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    MODELS_OUTPUT_FILE = BASE_OUTPUT_DIR / "models.py"
    FACADE_OUTPUT_FILE = BASE_OUTPUT_DIR / "facade.py"
    ENDPOINTS_DIR = BASE_OUTPUT_DIR / "endpoints"
    ENDPOINTS_DIR.mkdir(exist_ok=True)

    definitions = swagger_dict.get("definitions", {})

    TYPE_MAPPING = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "number": "float",
        "object": "dict",
    }

    def convert_type(prop: Dict[str, Any]) -> str:
        """Преобразует описание типа Swagger в строковое представление типа Python."""
        if "$ref" in prop:
            return prop["$ref"].split("/")[-1]
        prop_type = prop.get("type")
        if prop_type == "array":
            items = prop.get("items", {})
            inner_type = convert_type(items)
            return f"List[{inner_type}]"
        return TYPE_MAPPING.get(prop_type, "Any")

    def generate_field(prop_name: str, details: Dict[str, Any], required: bool) -> str:
        """Генерирует строку для одного поля модели с использованием Field."""
        field_type = convert_type(details)
        if not required:
            field_type = f"Optional[{field_type}]"
        default = "..." if required else "None"
        field_args = []
        if "title" in details:
            field_args.append(f'title="{details["title"]}"')
        if "maxLength" in details:
            field_args.append(f"max_length={details['maxLength']}")
        if "minLength" in details:
            field_args.append(f"min_length={details['minLength']}")
        field_args_str = ", " + ", ".join(field_args) if field_args else ""
        return f"    {prop_name}: {field_type} = Field({default}{field_args_str})"

    def generate_model(model_name: str, model: Dict[str, Any]) -> str:
        """Генерирует класс модели Pydantic по описанию Swagger."""
        properties = model.get("properties", {})
        required_props = model.get("required", [])
        lines = [f"class {model_name}(BaseModel):"]
        if not properties:
            lines.append("    pass")
        else:
            for prop_name, details in properties.items():
                is_required = prop_name in required_props
                lines.append(generate_field(prop_name, details, is_required))
        return "\n".join(lines)

    models: List[str] = []
    for model_name, model in definitions.items():
        models.append(generate_model(model_name, model))

    # Шаблон для моделей (можно вынести в отдельный файл .jinja, но пока оставим прямо здесь)
    models_template_str = r'''from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime, date

{% for model in models %}
{{ model }}

{% endfor %}
'''
    template_models = Template(models_template_str)
    rendered_models = template_models.render(models=models)
    MODELS_OUTPUT_FILE.write_text(rendered_models, encoding="utf-8")
    print(f"[Django] Модели сгенерированы в {MODELS_OUTPUT_FILE}")

    paths = swagger_dict.get("paths", {})
    http_methods = {"get", "post", "put", "delete", "patch"}
    methods_list: List[Dict[str, Any]] = []

    for path, methods in paths.items():
        for method, details in methods.items():
            if method.lower() not in http_methods:
                continue
            parameters = details.get("parameters", [])
            path_params = [p for p in parameters if p.get("in") == "path"]
            body_params = [p for p in parameters if p.get("in") == "body"]

            operation_id = details.get("operationId")
            if not operation_id:
                op_suffix = path.strip("/").replace("/", "_").replace("{", "").replace("}", "")
                operation_id = f"{method.lower()}_{op_suffix}"

            description = details.get("description", operation_id)
            if description:
                description = description.replace("\n", " ").strip()
            else:
                description = operation_id

            tags = details.get("tags", [])
            tag = tags[0] if tags else "default"

            response_model = None
            responses = details.get("responses", {})
            for code in ("200", "201"):
                if code in responses:
                    schema = responses[code].get("schema", {})
                    if "$ref" in schema:
                        response_model = schema["$ref"].split("/")[-1]
                        break
            if not response_model:
                response_model = "Any"

            payload_type = None
            if body_params:
                payload_type = "dict"

            method_parameters = []
            for p in path_params:
                method_parameters.append(f"{p['name']}: str")

            methods_list.append({
                "name": operation_id,
                "description": description,
                "method_parameters": method_parameters,
                "http_method": method.upper(),
                "payload_type": payload_type,
                "expected_status": "OK",
                "return_type": response_model,
                "path": path,
                "tag": tag,
            })

    base_path = swagger_dict.get("basePath", "")

    endpoints_by_tag: Dict[str, List[Dict[str, Any]]] = {}
    for m in methods_list:
        tag = m.get("tag", "default")
        endpoints_by_tag.setdefault(tag, []).append(m)

    endpoint_template_path = Path("endpoint_template.jinja")
    if not endpoint_template_path.exists():
        raise FileNotFoundError("Файл шаблона endpoint_template.jinja не найден.")

    endpoint_template_str = endpoint_template_path.read_text(encoding="utf-8")
    endpoint_template = Template(endpoint_template_str)

    models_import_path = f"http_clients.{Path(base_output_dir).name}.models"

    imports_list = list(definitions.keys())

    for tag, methods in endpoints_by_tag.items():
        class_name = f"{tag.capitalize()}"
        service_name = base_path
        rendered_class = endpoint_template.render(
            models_import_path=models_import_path,
            imports=imports_list,
            class_name=class_name,
            service_name=service_name,
            methods=methods
        )
        output_file = ENDPOINTS_DIR / f"{tag.lower()}_client.py"
        output_file.write_text(rendered_class, encoding="utf-8")
        print(f"[Django] Код для группы '{tag}' сгенерирован в {output_file}")

    facade_template_path = Path("facade_template.jinja")
    if not facade_template_path.exists():
        raise FileNotFoundError("Файл шаблона facade_template.jinja не найден.")

    facade_template_str = facade_template_path.read_text(encoding="utf-8")
    facade_template = Template(facade_template_str)

    facade_imports = []
    for tag in endpoints_by_tag.keys():
        facade_imports.append({
            "module_name": f"{tag.lower()}_client",
            "class_name": f"{tag.capitalize()}",
            "attribute_name": tag.lower()
        })

    rendered_facade = facade_template.render(
        imports=facade_imports,
        facade_class_name="ApiFacade"
    )
    FACADE_OUTPUT_FILE.write_text(rendered_facade, encoding="utf-8")
    print(f"[Django] Фасад сгенерирован в {FACADE_OUTPUT_FILE}")

    print("[Django] Генерация завершена.")
