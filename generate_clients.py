# import os
# import re
# import json
# import subprocess
# import sys
# from dataclasses import dataclass, field
# from http import HTTPStatus
# from typing import List, Dict, Any, Optional
#
# from jinja2 import Environment, FileSystemLoader
#
# # =============== DATA CLASSES ===============
#
# @dataclass
# class Parameter:
#     """
#     Базовый класс для параметра (path, query).
#     """
#     name: str
#     type: str
#     required: bool = False
#
#
# @dataclass
# class Endpoint:
#     """
#     Класс для представления информации об одном эндпоинте.
#     """
#     tag: str
#     name: str
#     http_method: str
#     path: str
#     path_params: List[Parameter] = field(default_factory=list)
#     query_params: List[Parameter] = field(default_factory=list)
#     payload_type: Optional[str] = None
#     expected_status: str = "OK"
#     return_type: str = "Any"
#     description: str = ""
#
#     @property
#     def sanitized_path(self) -> str:
#         """Гарантируем, что путь начинается с '/'."""
#         return self.path if self.path.startswith('/') else f'/{self.path}'
#
#     @property
#     def method_parameters(self) -> List[str]:
#         """Собирает параметры метода (path_params, query_params) в виде 'name: type'."""
#         return [f"{param.name}: {param.type}" for param in self.path_params if param.required]
#
#
# @dataclass
# class SubPath:
#     """
#     Класс для представления дополнительного подпути внутри базового пути.
#     Например: /search, /{step_oid}, ...
#     """
#     name: str
#     path: str
#
#
# # =============== HELPERS ===============
#
# def run_command(command: str, cwd: Optional[str] = None) -> None:
#     """Запуск shell-команды."""
#     print(f"Running command: {command}")
#     try:
#         subprocess.run(command, shell=True, check=True, cwd=cwd)
#     except subprocess.CalledProcessError as e:
#         print(f"An error occurred while running command: {command}\nError: {e}")
#         sys.exit(e.returncode)
#     else:
#         print("Command executed successfully.\n")
#
# def remove_underscores(name: str) -> str:
#     """Убирает 'лишние' подчёркивания из имени, пытаясь сохранить CamelCase."""
#     segments = name.split('_')
#     cleaned_segments = []
#     for seg in segments:
#         seg = seg.strip()
#         if not seg:
#             continue
#         if re.match(r'^[A-Z][a-zA-Z0-9]*$', seg):
#             cleaned_segments.append(seg)
#         else:
#             cleaned_segments.append(seg.capitalize())
#     return ''.join(cleaned_segments)
#
#
# # =============== OOP CLASSES ===============
#
# class SwaggerLoader:
#     """
#     Класс, отвечающий за чтение и первоначальную обработку Swagger.
#     """
#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         self.swagger: Dict[str, Any] = {}
#
#     def load(self) -> None:
#         """Считываем Swagger-файл в self.swagger."""
#         with open(self.file_path, 'r', encoding='utf-8') as f:
#             self.swagger = json.load(f)
#
#     def get_swagger_dict(self) -> Dict[str, Any]:
#         """Возвращает считанный swagger-словарь."""
#         return self.swagger
#
#     def get_service_name(self) -> str:
#         """Извлекает название сервиса из swagger['info']['title']."""
#         info = self.swagger.get("info", {})
#         title = info.get("title", "default")
#         return title.strip().lower().replace(' ', '_')
#
#
# class SwaggerProcessor:
#     """
#     Класс, который умеет извлекать эндпоинты, схемы, базовые пути из swagger.
#     """
#     def __init__(self, swagger: Dict[str, Any]):
#         self.swagger = swagger
#
#     def extract_endpoints(self) -> List[Endpoint]:
#         endpoints: List[Endpoint] = []
#         paths = self.swagger.get('paths', {})
#
#         for path, methods in paths.items():
#             for http_method, details in methods.items():
#                 tags = details.get('tags', ['default'])
#                 for tag in tags:
#                     method_name = self.determine_method_name(http_method, path, details)
#                     description = details.get('description', details.get('summary', ''))
#
#                     parameters = details.get('parameters', [])
#                     path_params = self.extract_parameters(parameters, 'path')
#                     query_params = self.extract_parameters(parameters, 'query')
#
#                     # Извлечение тела запроса
#                     request_body = details.get('requestBody', {})
#                     payload_type = None
#                     if request_body:
#                         content = request_body.get('content', {})
#                         for ctype_key in ('application/json', 'multipart/form-data'):
#                             if ctype_key in content:
#                                 schema = content[ctype_key].get('schema', {})
#                                 payload_type = self.map_openapi_type_to_python(schema)
#                                 break
#
#                     # Извлечение ответа
#                     responses = details.get('responses', {})
#                     expected_status = 'OK'
#                     return_type = 'Any'
#                     for status_code, response_obj in responses.items():
#                         if status_code.startswith('2'):
#                             expected_status = self.get_http_status_enum(status_code)
#                             resp_content = response_obj.get('content', {})
#                             if 'application/json' in resp_content:
#                                 schema = resp_content['application/json'].get('schema', {})
#                                 return_type = self.map_openapi_type_to_python(schema)
#                             elif 'application/octet-stream' in resp_content:
#                                 return_type = 'bytes'
#                             elif 'text/plain' in resp_content:
#                                 return_type = 'str'
#                             break
#
#                     endpoints.append(
#                         Endpoint(
#                             tag=tag,
#                             name=method_name,
#                             http_method=http_method.upper(),
#                             path=path,
#                             path_params=path_params,
#                             query_params=query_params,
#                             payload_type=payload_type,
#                             expected_status=expected_status,
#                             return_type=return_type,
#                             description=description
#                         )
#                     )
#         return endpoints
#
#     def extract_imports(self) -> List[str]:
#         """Извлекает названия схем из swagger (components/schemas), убирая подчёркивания."""
#         components = self.swagger.get('components', {})
#         schemas = components.get('schemas', {})
#         return [remove_underscores(name) for name in schemas.keys()]
#
#     @staticmethod
#     def get_http_status_enum(status_code: str) -> str:
#         try:
#             return HTTPStatus(int(status_code)).name
#         except ValueError:
#             return 'OK'
#
#     @staticmethod
#     def map_openapi_type_to_python(schema: Dict[str, Any]) -> str:
#         if '$ref' in schema:
#             raw_name = schema['$ref'].split('/')[-1]
#             clean_name = remove_underscores(raw_name)
#             return clean_name
#
#         openapi_type = schema.get('type', 'Any')
#         if openapi_type == 'array':
#             items = schema.get('items', {})
#             return f"List[{SwaggerProcessor.map_openapi_type_to_python(items)}]"
#
#         type_mapping = {
#             'string': 'str',
#             'integer': 'int',
#             'number': 'float',
#             'boolean': 'bool',
#             'object': 'Dict[str, Any]',
#             'any': 'Any'
#         }
#         return type_mapping.get(openapi_type, 'Any')
#
#     @staticmethod
#     def extract_parameters(parameters: List[Dict[str, Any]], location: str) -> List[Parameter]:
#         result = []
#         for param in parameters:
#             if param.get('in') == location:
#                 schema = param.get('schema', {})
#                 result.append(
#                     Parameter(
#                         name=param.get('name'),
#                         type=SwaggerProcessor.map_openapi_type_to_python(schema),
#                         required=param.get('required', False)
#                     )
#                 )
#         return result
#
#     @staticmethod
#     def determine_method_name(http_method: str, path: str, details: Dict[str, Any]) -> str:
#         summary = details.get('summary', '')
#         operation_id = details.get('operationId', '')
#
#         if summary:
#             raw_name = summary
#         elif operation_id:
#             raw_name = operation_id
#         else:
#             raw_name = f"{http_method}_{path.strip('/').replace('/', '_').replace('{', '').replace('}', '')}"
#
#         method_name = re.sub(r'[^a-zA-Z0-9]+', '_', raw_name.strip().lower()).strip('_')
#         return method_name
#
#
# class ClientGenerator:
#     """
#     Генерирует Python-клиенты на основе списка Endpoints.
#     """
#     def __init__(self, endpoints: List[Endpoint], imports: List[str], template_path: str):
#         self.endpoints = endpoints
#         self.imports = imports
#         self.template_path = template_path
#
#         # Готовим окружение jinja
#         self.env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
#         self.template = self.env.get_template(self.template_path)
#
#     def generate_clients(self, output_dir: str) -> Dict[str, str]:
#         """
#         Проходит по всем эндпоинтам, группирует по тегам, рендерит файлы.
#         Возвращает { filename: className } для дальнейшего использования в фасаде.
#         """
#         os.makedirs(output_dir, exist_ok=True)
#
#         grouped = self.group_endpoints_by_tag(self.endpoints)
#         file_to_class: Dict[str, str] = {}
#
#         for tag, eps in grouped.items():
#             class_name = self.class_name_from_tag(tag)
#             base_path = self.determine_base_path(eps)
#
#             sub_paths = self._collect_sub_paths(eps, base_path)
#
#             # Рендер
#             rendered = self.template.render(
#                 class_name=class_name,
#                 base_path=base_path,
#                 sub_paths=sub_paths,
#                 methods=eps,
#                 imports=self.imports
#             )
#
#             filename = f"{class_name.lower()}_client.py"
#             full_path = os.path.join(output_dir, filename)
#             with open(full_path, 'w', encoding='utf-8') as f:
#                 f.write(rendered)
#             print(f"[OK] Сгенерирован клиент: {filename}")
#             file_to_class[filename] = class_name
#
#         return file_to_class
#
#     @staticmethod
#     def group_endpoints_by_tag(endpoints: List[Endpoint]) -> Dict[str, List[Endpoint]]:
#         grouped: Dict[str, List[Endpoint]] = {}
#         for ep in endpoints:
#             grouped.setdefault(ep.tag, []).append(ep)
#         return grouped
#
#     @staticmethod
#     def class_name_from_tag(tag: str) -> str:
#         """Перевод тега в CamelCase."""
#         tag = tag.replace('-', '_')
#         parts = re.split(r'[\s_]+', tag)
#         return ''.join(word.capitalize() for word in parts if word)
#
#     @staticmethod
#     def determine_base_path(eps: List[Endpoint]) -> str:
#         paths = [ep.path for ep in eps]
#         if not paths:
#             return '/'
#         split_paths = [p.strip('/').split('/') for p in paths]
#         common = split_paths[0]
#         for sp in split_paths[1:]:
#             min_length = min(len(common), len(sp))
#             temp = []
#             for i in range(min_length):
#                 if common[i] == sp[i]:
#                     temp.append(common[i])
#                 else:
#                     break
#             common = temp
#         return '/' + '/'.join(common)
#
#     def _collect_sub_paths(self, eps: List[Endpoint], base_path: str) -> List[SubPath]:
#         sub_paths: List[SubPath] = []
#
#         for ep in eps:
#             path_suffix = ep.sanitized_path
#             if path_suffix.startswith(base_path):
#                 path_suffix = ep.sanitized_path[len(base_path):]
#
#             if not path_suffix.startswith('/'):
#                 path_suffix = '/' + path_suffix
#
#             if path_suffix and path_suffix != '/':
#                 sub_path_name = self._extract_sub_path_name(path_suffix)
#                 if sub_path_name not in [sp.name for sp in sub_paths]:
#                     sub_paths.append(SubPath(name=sub_path_name, path=path_suffix))
#         return sub_paths
#
#     @staticmethod
#     def _extract_sub_path_name(sub_path: str) -> str:
#         segments = sub_path.strip('/').split('/')
#         if segments:
#             first_segment = segments[0]
#             if first_segment.startswith('{') and first_segment.endswith('}'):
#                 return first_segment[1:-1]
#             return first_segment
#         return 'sub_path'
#
#
# class FacadeGenerator:
#     """
#     Генерирует фасадный класс (например, CdeApi) на основе уже сгенерированных файлов
#     и их соответствия file -> className.
#     """
#     def __init__(self, facade_class_name: str, template_path: str):
#         self.facade_class_name = facade_class_name
#         self.template_path = template_path
#         self.env = Environment(loader=FileSystemLoader('.'), trim_blocks=True, lstrip_blocks=True)
#         self.template = self.env.get_template(self.template_path)
#
#     def generate_facade(self, file_to_class: Dict[str, str], output_dir: str, file_name: str) -> None:
#         client_files = sorted(fname for fname in file_to_class if fname.endswith("_client.py"))
#         imports_data = []
#         for fname in client_files:
#             module_name = fname[:-3]      # e.g. "accesspasses_client"
#             class_name = file_to_class[fname]  # e.g. "AccessPasses"
#             attribute_name = class_name.lower() # e.g. "accesspasses"
#             imports_data.append({
#                 "module_name": module_name,
#                 "class_name": class_name,
#                 "attribute_name": attribute_name,
#             })
#
#         rendered = self.template.render(
#             facade_class_name=self.facade_class_name,
#             imports=imports_data,
#             docstring_indent="    "
#         )
#
#         facade_file_path = os.path.join(output_dir, file_name)
#         with open(facade_file_path, "w", encoding="utf-8") as f:
#             f.write(rendered)
#
#         print(f"[OK] Facade class {self.facade_class_name} сгенерирован в {facade_file_path}")
#
#
# class ModelGenerator:
#     """
#     Генерация Pydantic-моделей (через datamodel-codegen), а также пост-обработка кода.
#     """
#     def __init__(self, swagger_path: str, models_file: str = 'models.py'):
#         self.swagger_path = swagger_path
#         self.models_file = models_file
#
#     def generate_models(self) -> None:
#         """Выкачиваем swagger.json и генерируем модели datamodel-codegen."""
#         # Пример команды (замените URL при необходимости)
#         # swagger_cmd = "curl https://lahta.uat.simple-solution.liis.su/checkpoint/openapi.json -o ./swagger.json"
#         swagger_cmd = "curl https://lahta.uat.simple-solution.liis.su/cde/openapi.json -o ./swagger.json"
#         model_cmd = (
#             f"datamodel-codegen --input {self.swagger_path} "
#             "--input-file-type openapi "
#             "--output models.py "
#             "--reuse-model "
#             "--use-title-as-name "
#             "--use-schema-description "
#             "--collapse-root-models "
#             "--target-python-version 3.9"
#         )
#         run_command(swagger_cmd)
#         run_command(model_cmd)
#
#     def fix_models_inheritance(self) -> None:
#         """Правим BaseModel -> BaseConfigModel (пример)."""
#         if not os.path.exists(self.models_file):
#             print(f"[WARN] {self.models_file} not found, skip fix.")
#             return
#
#         with open(self.models_file, 'r', encoding='utf-8') as f:
#             lines = f.readlines()
#
#         new_lines = []
#         found_pydantic_config_import = False
#         base_model_pattern = re.compile(r"\bBaseModel\b")
#         last_import_index = -1
#
#         for idx, line in enumerate(lines):
#             stripped = line.strip()
#             if stripped.startswith("import ") or stripped.startswith("from "):
#                 last_import_index = len(new_lines)
#
#             line = base_model_pattern.sub("BaseConfigModel", line)
#
#             if stripped.startswith("from pydantic import"):
#                 prefix = "from pydantic import "
#                 after_import = stripped[len(prefix):]
#                 imports_list = [imp.strip() for imp in after_import.split(",")]
#                 filtered_imports = [imp for imp in imports_list if imp not in ("BaseModel", "BaseConfigModel")]
#
#                 if len(filtered_imports) == 0:
#                     continue
#                 else:
#                     new_line = prefix + ", ".join(filtered_imports) + "\n"
#                     new_lines.append(new_line)
#             else:
#                 if "from pydantic_config import BaseConfigModel" in line:
#                     found_pydantic_config_import = True
#                 new_lines.append(line)
#
#         if not found_pydantic_config_import:
#             import_line = "from pydantic_config import BaseConfigModel\n"
#             if last_import_index >= 0:
#                 new_lines.insert(last_import_index + 1, import_line)
#             else:
#                 new_lines.insert(0, import_line)
#
#         with open(self.models_file, 'w', encoding='utf-8') as f:
#             f.writelines(new_lines)
#
#         print(f"[INFO] Fixed inheritance in {self.models_file}")
#
#     def post_process_code(self, output_dir: str) -> None:
#         """
#         Запускает autoflake и black для рефакторинга кода.
#         """
#         autoflake_cmd = (
#             "autoflake "
#             "--remove-all-unused-imports "
#             "--recursive "
#             "--in-place "
#             f"'{output_dir}'"
#         )
#         black_cmd = f"black '{output_dir}'"
#
#         run_command(autoflake_cmd)
#         run_command(black_cmd)
#
#
# class GeneratorOrchestrator:
#     """
#     Высокоуровневый класс, объединяющий всю логику:
#     - загрузка Swagger
#     - генерация моделей
#     - генерация клиентов
#     - генерация фасада
#     """
#     def __init__(self, swagger_path: str, base_output_dir: str = "http_clients"):
#         self.swagger_path = swagger_path
#         self.base_output_dir = base_output_dir
#
#     def run(self):
#         # 1. Загрузка Swagger
#         loader = SwaggerLoader(self.swagger_path)
#         loader.load()
#         swagger_dict = loader.get_swagger_dict()
#         service_name = loader.get_service_name()
#
#         # 2. Генерация и фиксы Pydantic-моделей
#         model_gen = ModelGenerator(self.swagger_path, models_file='models.py')
#         model_gen.generate_models()
#         model_gen.fix_models_inheritance()
#
#         # 3. Создаём директорию для сервиса
#         service_dir = os.path.join(self.base_output_dir, service_name)
#         os.makedirs(service_dir, exist_ok=True)
#
#         # 4. Парсим Swagger -> Endpoints, Schemas
#         processor = SwaggerProcessor(swagger_dict)
#         endpoints = processor.extract_endpoints()
#         imports = processor.extract_imports()
#
#         # 5. Генерация клиентов
#         client_gen = ClientGenerator(endpoints, imports, template_path='templates/client_template.j2')
#         file_to_class = client_gen.generate_clients(service_dir)
#
#         # 6. Форматируем код
#         model_gen.post_process_code(service_dir)
#
#         # 7. Генерируем фасад
#         facade_gen = FacadeGenerator(
#             facade_class_name=f"{service_name.capitalize()}Api",
#             template_path='templates/facade_template.j2'
#         )
#         facade_filename = f"{service_name}_facade.py"
#         facade_gen.generate_facade(file_to_class, service_dir, facade_filename)
#
#         print(f"\n[DONE] Клиенты и фасад для сервиса '{service_name}' готовы: {service_dir}")
#
#
# # =============== MAIN SCRIPT ===============
#
# def main():
#     orchestrator = GeneratorOrchestrator(swagger_path='swagger.json', base_output_dir='http_clients')
#     orchestrator.run()
#
# if __name__ == "__main__":
#     main()
