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
    loader.load()
    swagger_dict = loader.get_swagger_dict()
    service_name = loader.get_service_name()

    # Генерация Pydantic-моделей
    model_gen = ModelGenerator(swagger_path, 'models.py')
    model_gen.generate_models()
    model_gen.fix_models_inheritance()

    # Директория для генерации
    base_output_dir = 'http_clients'
    service_dir = os.path.join(base_output_dir, service_name)
    os.makedirs(service_dir, exist_ok=True)

    # Парсинг Swagger
    processor = SwaggerProcessor(swagger_dict)
    endpoints = processor.extract_endpoints()  # List[Endpoint]
    imports = processor.extract_imports()      # List[str]

    # Генерация клиентов
    client_gen = ClientGenerator(
        endpoints=endpoints,
        imports=imports,
        template_path='templates/client_template.j2'
    )
    file_to_class = client_gen.generate_clients(service_dir)

    # Автоформат
    model_gen.post_process_code(service_dir)

    # Генерация фасада
    facade_gen = FacadeGenerator(
        facade_class_name=f"{service_name.capitalize()}Api",
        template_path='templates/facade_template.j2'
    )
    facade_filename = f"{service_name}_facade.py"
    facade_gen.generate_facade(file_to_class, service_dir, facade_filename)

    print(f"\n[DONE] Клиенты и фасад для сервиса '{service_name}' готовы: {service_dir}")

if __name__ == "__main__":
    main()
