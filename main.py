import os
from swagger.loader import SwaggerLoader
from swagger.processor import SwaggerProcessor
from codegen.client_generator import ClientGenerator
from codegen.facade_generator import FacadeGenerator
from codegen.data_models import Endpoint
from model_generator import ModelGenerator


def main():
    swagger_path = 'swagger.json'
    loader = SwaggerLoader(swagger_path)

    # 1. Скачиваем swagger
    loader.download_swagger(url='https://lahta.uat.simple-solution.liis.su/checkpoint/openapi.json')
    loader.load()
    swagger_dict = loader.get_swagger_dict()
    service_name = loader.get_service_name()  # "checkpoint"

    # 2. Создаём структуру директорий
    base_output_dir = 'http_clients'
    service_dir = os.path.join(base_output_dir, service_name)
    endpoints_dir = os.path.join(service_dir, "endpoints")
    os.makedirs(service_dir, exist_ok=True)
    os.makedirs(endpoints_dir, exist_ok=True)

    # 3. Генерация моделей -> http_clients/checkpoint/models.py
    models_file = os.path.join(service_dir, "models")  # "models"
    model_gen = ModelGenerator(swagger_path, models_file)
    model_gen.generate_models()
    model_gen.fix_models_inheritance()

    # 4. Парсинг
    processor = SwaggerProcessor(swagger_dict)
    endpoints = processor.extract_endpoints()  # List[Endpoint]
    imports = processor.extract_imports()  # List[str]

    # 5. Генерация клиентов -> http_clients/checkpoint/endpoints/*.py
    client_gen = ClientGenerator(
        endpoints=endpoints,
        imports=imports,
        template_path='templates/client_template.j2'
    )
    file_to_class = client_gen.generate_clients(endpoints_dir, service_name)

    # 6. Автоформат (применится ко всей папке service_dir, включая endpoints)
    model_gen.post_process_code(service_dir)

    # 7. Генерация фасада -> http_clients/checkpoint/facade.py
    facade_gen = FacadeGenerator(
        facade_class_name=f"{service_name.capitalize()}Api",
        template_path='templates/facade_template.j2'
    )
    facade_filename = "facade.py"  # вместо f"{service_name}_facade.py"
    facade_gen.generate_facade(file_to_class, service_dir, facade_filename)

    print(f"\n[DONE] Клиенты (endpoints/*.py), models и фасад для сервиса '{service_name}' готовы в {service_dir}")


if __name__ == "__main__":
    main()
