import os
import re
import json
import subprocess
import sys
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import List, Dict, Any, Optional

from jinja2 import Environment, FileSystemLoader


# =======================
# Data classes & helpers
# =======================

@dataclass
class Parameter:
    """
    Базовый класс для параметра (path, query).
    """
    name: str
    type: str
    required: bool = False


@dataclass
class Endpoint:
    """
    Класс для представления информации об одном эндпоинте.
    """
    tag: str
    name: str
    http_method: str
    path: str
    path_params: List[Parameter] = field(default_factory=list)
    query_params: List[Parameter] = field(default_factory=list)
    payload_type: Optional[str] = None
    expected_status: str = "OK"
    return_type: str = "Any"
    description: str = ""

    @property
    def sanitized_path(self) -> str:
        """Возвращает путь, гарантируя, что он всегда начинается с '/'. """
        return self.path if self.path.startswith('/') else f'/{self.path}'

    @property
    def method_parameters(self) -> List[str]:
        """
        Собирает параметры метода (path_params, query_params и т.п.) в виде "name: type".
        """
        return [f"{param.name}: {param.type}" for param in self.path_params if param.required]


@dataclass
class SubPath:
    """
    Класс для представления дополнительного подпути внутри базового пути.
    Например, /search или /{step_oid}.
    """
    name: str
    path: str


# =======================
# Swagger & code helpers
# =======================

def load_swagger(file_path: str) -> Dict[str, Any]:
    """Загружает спецификацию из JSON-файла."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_service_name(swagger: Dict[str, Any]) -> str:
    """
    Извлекает название сервиса из swagger["info"]["title"].
    Если нет, возвращает 'default'.
    """
    info = swagger.get("info", {})
    title = info.get("title", "default")
    return title.strip().lower().replace(' ', '_')  # на случай пробелов в названии


def generate_facade_class(
        file_to_class: Dict[str, str],  # <-- вместо вычислений берем готовые данные
        output_dir: str,
        facade_class_name: str = "CdeApi",
        template_path: str = "facade_template.j2",
        file_name='cde_api.py'
) -> None:
    """
    Создаёт единый фасадный класс, который импортирует все *_client.py классы
    и собирает их в одном месте. Запишет в 'cde_api.py' (по умолчанию).

    file_to_class: маппинг {filename: className} от generate_clients.
    """
    # 1. Собираем файлы *_client.py
    #    Но теперь нам не надо искать класс: у нас уже есть file_to_class
    client_files = sorted(fname for fname in file_to_class if fname.endswith("_client.py"))

    imports_data = []
    for fname in client_files:
        module_name = fname[:-3]  # e.g. "accesspasses_client"
        class_name = file_to_class[fname]  # e.g. "AccessPasses"
        # Пусть attribute_name = class_name.lower() или ...
        # или можно base = module_name.replace("_client", ""), а затем ...
        attribute_name = class_name.lower()  # "accesspasses"
        # Если хотите snake_case: "approval_process_templates"
        # тогда придется "reverse-engineer" .splitCamelCase -> snake

        imports_data.append({
            "module_name": module_name,
            "class_name": class_name,
            "attribute_name": attribute_name,
        })

    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_path)

    rendered = template.render(
        facade_class_name=facade_class_name,
        imports=imports_data,
        docstring_indent="    "
    )

    facade_file_path = os.path.join(output_dir, file_name)
    with open(facade_file_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[OK] Facade class {facade_class_name} сгенерирован в {facade_file_path}")


def get_http_status_enum(status_code: str) -> str:
    """Маппит статус-код в enum HTTPStatus (если возможно)."""
    try:
        return HTTPStatus(int(status_code)).name
    except ValueError:
        return 'OK'


def remove_underscores(name: str) -> str:
    """
    Убирает «лишние» подчёркивания внутри названия схемы,
    пытаясь сохранить CamelCase, если оно есть.
    """
    segments = name.split('_')
    cleaned_segments = []
    for seg in segments:
        seg = seg.strip()
        if not seg:
            continue
        # Если сегмент уже похож на CamelCase, оставим как есть:
        if re.match(r'^[A-Z][a-zA-Z0-9]*$', seg):
            cleaned_segments.append(seg)
        else:
            # Иначе просто делаем .capitalize()
            cleaned_segments.append(seg.capitalize())
    return ''.join(cleaned_segments)


def map_openapi_type_to_python(schema: Dict[str, Any]) -> str:
    """
    Преобразует openapi-тип в соответствующий Python-тип (str, int, List[...] и т.д.).
    Плюс выполняется «очистка» имён схем (убираем подчёркивания и т.д.).
    """
    if '$ref' in schema:
        raw_name = schema['$ref'].split('/')[-1]
        clean_name = remove_underscores(raw_name)
        return clean_name

    openapi_type = schema.get('type', 'Any')
    if openapi_type == 'array':
        items = schema.get('items', {})
        return f"List[{map_openapi_type_to_python(items)}]"

    type_mapping = {
        'string': 'str',
        'integer': 'int',
        'number': 'float',
        'boolean': 'bool',
        'object': 'Dict[str, Any]',
        'any': 'Any'
    }
    return type_mapping.get(openapi_type, 'Any')


def extract_parameters(parameters: List[Dict[str, Any]], location: str) -> List[Parameter]:
    """
    Универсальная функция для извлечения параметров по месту (in=path или in=query).
    """
    result = []
    for param in parameters:
        if param.get('in') == location:
            schema = param.get('schema', {})
            result.append(
                Parameter(
                    name=param.get('name'),
                    type=map_openapi_type_to_python(schema),
                    required=param.get('required', False)
                )
            )
    return result


def determine_method_name(http_method: str, path: str, details: Dict[str, Any]) -> str:
    """
    Формирует имя метода на основе:
     - summary (приоритет),
     - operationId (если нет summary),
     - fallback-значения (если нет ни summary, ни operationId).
    После получения «сырого» имени приводим его к нижнему регистру,
    заменяя любые не alnum/underscore/digit на '_'.
    """
    summary = details.get('summary', '')
    operation_id = details.get('operationId', '')

    if summary:
        raw_name = summary
    elif operation_id:
        raw_name = operation_id
    else:
        raw_name = f"{http_method}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}"

    method_name = re.sub(r'[^a-zA-Z0-9]+', '_', raw_name.strip().lower()).strip('_')
    return method_name


def extract_endpoints(swagger: Dict[str, Any]) -> List[Endpoint]:
    """
    Извлекает все эндпоинты из swagger и превращает их в объекты Endpoint.
    """
    endpoints: List[Endpoint] = []
    paths = swagger.get('paths', {})

    for path, methods in paths.items():
        for http_method, details in methods.items():
            tags = details.get('tags', ['default'])
            for tag in tags:
                method_name = determine_method_name(http_method, path, details)
                description = details.get('description', details.get('summary', ''))

                parameters = details.get('parameters', [])
                path_params = extract_parameters(parameters, 'path')
                query_params = extract_parameters(parameters, 'query')

                # Извлечение тела запроса
                request_body = details.get('requestBody', {})
                payload_type = None
                if request_body:
                    content = request_body.get('content', {})
                    for ctype_key in ('application/json', 'multipart/form-data'):
                        if ctype_key in content:
                            schema = content[ctype_key].get('schema', {})
                            payload_type = map_openapi_type_to_python(schema)
                            break

                # Извлечение ответа
                responses = details.get('responses', {})
                expected_status = 'OK'
                return_type = 'Any'
                for status_code, response_obj in responses.items():
                    if status_code.startswith('2'):
                        expected_status = get_http_status_enum(status_code)
                        resp_content = response_obj.get('content', {})
                        if 'application/json' in resp_content:
                            schema = resp_content['application/json'].get('schema', {})
                            return_type = map_openapi_type_to_python(schema)
                        elif 'application/octet-stream' in resp_content:
                            return_type = 'bytes'
                        elif 'text/plain' in resp_content:
                            return_type = 'str'
                        break

                endpoints.append(
                    Endpoint(
                        tag=tag,
                        name=method_name,
                        http_method=http_method.upper(),
                        path=path,
                        path_params=path_params,
                        query_params=query_params,
                        payload_type=payload_type,
                        expected_status=expected_status,
                        return_type=return_type,
                        description=description
                    )
                )

    return endpoints


def extract_imports(swagger: Dict[str, Any]) -> List[str]:
    """
    Извлекает названия схем из swagger (components/schemas) для последующего использования в импортах,
    убирая из них подчёркивания.
    """
    components = swagger.get('components', {})
    schemas = components.get('schemas', {})
    return [remove_underscores(name) for name in schemas.keys()]


def class_name_from_tag(tag: str) -> str:
    """
    Преобразует тег в CamelCase для названия класса,
    предварительно заменяя '-' на '_'.
    """
    tag = tag.replace('-', '_')
    parts = re.split(r'[\s_]+', tag)
    return ''.join(word.capitalize() for word in parts if word)


def determine_base_path(endpoints: List[Endpoint]) -> str:
    """
    Вычисляет общий базовый путь для эндпоинтчов (если он есть).
    """
    paths = [ep.path for ep in endpoints]
    if not paths:
        return '/'

    split_paths = [p.strip('/').split('/') for p in paths]
    common = split_paths[0]
    for sp in split_paths[1:]:
        min_length = min(len(common), len(sp))
        temp = []
        for i in range(min_length):
            if common[i] == sp[i]:
                temp.append(common[i])
            else:
                break
        common = temp
    return '/' + '/'.join(common)


def extract_sub_path_name(sub_path: str) -> str:
    """
    Преобразует подпуть в имя.
    Пример: '/search' -> 'search', '/steps/{step_oid}' -> 'steps'
    """
    segments = sub_path.strip('/').split('/')
    if segments:
        first_segment = segments[0]
        if first_segment.startswith('{') and first_segment.endswith('}'):
            return first_segment[1:-1]
        return first_segment
    return 'sub_path'


def group_endpoints_by_tag(endpoints: List[Endpoint]) -> Dict[str, List[Endpoint]]:
    """
    Группирует список эндпоинтов по их тегам.
    """
    grouped: Dict[str, List[Endpoint]] = {}
    for ep in endpoints:
        grouped.setdefault(ep.tag, []).append(ep)
    return grouped


# =======================
# Client generation
# =======================


def generate_clients(swagger: Dict[str, Any],
                     template_path: str = 'client_template.j2',
                     output_dir: str = 'generated_clients'
                    ) -> Dict[str, str]:
    """
    Генерирует Python-клиенты на основе swagger-спецификации и Jinja2-шаблона.
    Возвращает словарь: { 'approvalprocesstemplates_client.py': 'ApprovalProcessTemplates', ... }
    """
    endpoints = extract_endpoints(swagger)
    imports = extract_imports(swagger)
    grouped_by_tag = group_endpoints_by_tag(endpoints)

    env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_path)

    os.makedirs(output_dir, exist_ok=True)

    # Тут храним маппинг файл -> класс
    file_to_class = {}

    for tag, eps in grouped_by_tag.items():
        class_name = class_name_from_tag(tag)
        base_path = determine_base_path(eps)

        sub_paths = []
        for ep in eps:
            if ep.sanitized_path.startswith(base_path):
                path_suffix = ep.sanitized_path[len(base_path):]
            else:
                path_suffix = ep.sanitized_path

            if not path_suffix.startswith('/'):
                path_suffix = '/' + path_suffix

            if path_suffix and path_suffix != '/':
                sub_path_name = extract_sub_path_name(path_suffix)
                if sub_path_name not in [sp.name for sp in sub_paths]:
                    sub_paths.append(SubPath(name=sub_path_name, path=path_suffix))

        # Рендер
        rendered = template.render(
            class_name=class_name,
            base_path=base_path,
            sub_paths=sub_paths,
            methods=eps,
            imports=imports
        )

        # Файл
        output_file = f"{class_name.lower()}_client.py"
        file_path = os.path.join(output_dir, output_file)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(f"[OK] Сгенерирован клиент: {output_file}")

        # Сохраняем, что именно в этом файле лежит класс class_name
        file_to_class[output_file] = class_name

    return file_to_class



# =======================
# Shell helpers
# =======================

def run_command(command: str, cwd: Optional[str] = None) -> None:
    """
    Runs a shell command, printing it before execution.
    Raises SystemExit on error.
    """
    print(f"Running command: {command}")
    try:
        subprocess.run(command, shell=True, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running command: {command}\nError: {e}")
        sys.exit(e.returncode)
    else:
        print("Command executed successfully.\n")


# =======================
# Main script logic
# =======================

def generate_models(swagger_path: str) -> None:
    """
    Генерация Pydantic-моделей при помощи `datamodel-codegen`.
    """
    swagger_cmd = "curl https://lahta.uat.simple-solution.liis.su/checkpoint/openapi.json -o ./swagger.json"
    # swagger_cmd = "curl https://lahta.uat.simple-solution.liis.su/cde/openapi.json -o ./swagger.json"
    model_cmd = (
        "datamodel-codegen "
        f"--input {swagger_path} "
        "--input-file-type openapi "
        "--output models.py "
        "--reuse-model "
        "--use-title-as-name "
        "--use-schema-description "
        "--collapse-root-models "
        "--target-python-version 3.9"
    )
    run_command(swagger_cmd)
    run_command(model_cmd)


def post_process_generated_code(output_dir: str) -> None:
    """
    Запускает autoflake и black для рефакторинга сгенерированного кода.
    """
    autoflake_cmd = (
        "autoflake "
        "--remove-all-unused-imports "
        "--recursive "
        "--in-place "
        f"'{output_dir}'"
    )
    black_cmd = f"black '{output_dir}'"

    run_command(autoflake_cmd)
    run_command(black_cmd)


def fix_models_inheritance(models_file_path: str) -> None:
    """
    Заменяем наследование BaseModel -> BaseConfigModel,
    удаляем BaseModel (и BaseConfigModel, если вдруг затесался) из строки импорта pydantic,
    и добавляем отдельный импорт 'from pydantic_config import BaseConfigModel'
    не в начало, а сразу после последнего import/... блока.
    """
    if not os.path.exists(models_file_path):
        print(f"[WARN] {models_file_path} not found, skip fix.")
        return

    with open(models_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    found_pydantic_config_import = False

    # Регулярка для замены "BaseModel" -> "BaseConfigModel" везде в тексте
    base_model_pattern = re.compile(r"\bBaseModel\b")

    last_import_index = -1

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("import ") or stripped.startswith("from "):
            last_import_index = len(new_lines)  # позиция в new_lines (не в исходном lines)

        # Меняем "BaseModel" -> "BaseConfigModel"
        line = base_model_pattern.sub("BaseConfigModel", line)

        # Если это строка вида "from pydantic import ..."
        if stripped.startswith("from pydantic import"):
            prefix = "from pydantic import "
            after_import = stripped[len(prefix):]  # всё, что после "from pydantic import "

            # Разделяем по запятым, убираем пробелы
            imports_list = [imp.strip() for imp in after_import.split(",")]

            # Убираем "BaseModel" и "BaseConfigModel" из списка
            filtered_imports = [
                imp for imp in imports_list
                if imp not in ("BaseModel", "BaseConfigModel")
            ]

            if len(filtered_imports) == 0:
                continue
            else:
                # Собираем новую строку импорта
                new_line = prefix + ", ".join(filtered_imports) + "\n"
                new_lines.append(new_line)
        else:
            # Проверяем, не появился ли уже "from pydantic_config import BaseConfigModel"
            if "from pydantic_config import BaseConfigModel" in line:
                found_pydantic_config_import = True

            new_lines.append(line)

    # Если нет импорта "from pydantic_config import BaseConfigModel", добавим
    if not found_pydantic_config_import:
        import_line = "from pydantic_config import BaseConfigModel\n"
        # Вставим строку сразу после последней «импортной» строки
        if last_import_index >= 0:
            # last_import_index указывает на индекс *в new_lines* последнего import
            new_lines.insert(last_import_index + 1, import_line)
        else:
            # если вовсе нет импортов, добавим в начало
            new_lines.insert(0, import_line)

    with open(models_file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"[INFO] Fixed inheritance in {models_file_path}")


def main():
    swagger_path = 'swagger.json'
    swagger_spec = load_swagger(swagger_path)
    service_name = get_service_name(swagger_spec)

    base_output_dir = 'http_clients'
    service_dir = os.path.join(base_output_dir, service_name)

    generate_models(swagger_path)
    fix_models_inheritance('models.py')

    # >>> ВАЖНО: Получаем mapping
    file_to_class = generate_clients(
        swagger_spec,
        template_path='templates/client_template.j2',
        output_dir=service_dir
    )

    post_process_generated_code(service_dir)

    # >>> Передаём mapping
    generate_facade_class(
        file_to_class=file_to_class,
        output_dir=service_dir,
        file_name=f'{service_name}_facade.py',        # e.g. "checkpoint_facade.py"
        facade_class_name=f"{service_name.capitalize()}Api",
        template_path="templates/facade_template.j2"
    )

    print(f"[DONE] Клиенты и фасад для сервиса '{service_name}' готовы: {service_dir}")


if __name__ == "__main__":
    main()