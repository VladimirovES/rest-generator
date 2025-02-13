import argparse
import os
from dotenv import load_dotenv

from my_codegen.swagger.loader import SwaggerLoader
from my_codegen.swagger.processor import SwaggerProcessor
from my_codegen.codegen.model_generator import ModelGenerator
from my_codegen.codegen.client_generator import ClientGenerator
from my_codegen.codegen.facade_generator import FacadeGenerator
from my_codegen.codegen.generate_app_facade import generate_app_facade
from my_codegen.codegen.django_generator import generate_django_code
from my_codegen.utils.logger import logger

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="API Client Generator")
    parser.add_argument(
        "--swagger-url",
        help="URL to download the Swagger JSON from",
        required=True
    )
    parser.add_argument(
        "--django",
        help="Generate Django-specific client code",
        action="store_true"
    )
    args = parser.parse_args()

    swagger_url = args.swagger_url
    logger.info(f"Swagger URL from CLI: {swagger_url}")

    # 1. Скачиваем и парсим swagger.json
    swagger_path = 'swagger.json'
    loader = SwaggerLoader(swagger_path)
    logger.info("Downloading Swagger file...")
    loader.download_swagger(url=swagger_url)
    logger.info("Swagger file downloaded. Now parsing the local swagger.json...")
    loader.load()
    swagger_dict = loader.swagger
    service_name = loader.get_service_name()
    logger.info(f"Service identified as: {service_name}")

    # 2. Создаем выходные директории: http_clients/<service_name>/ и endpoints/
    base_output_dir = 'http_clients'
    service_dir = os.path.join(base_output_dir, service_name)
    endpoints_dir = os.path.join(service_dir, "endpoints")
    os.makedirs(service_dir, exist_ok=True)
    os.makedirs(endpoints_dir, exist_ok=True)
    logger.info(f"Created directories: '{service_dir}' and '{endpoints_dir}'")

    # 3. Генерация моделей (в http_clients/<service_name>/models.py)
    models_file = os.path.join(service_dir, "models")
    model_gen = ModelGenerator(swagger_path, models_file)
    logger.info("Generating Pydantic models (via datamodel-codegen)...")
    model_gen.generate_models()
    logger.info("Fixing BaseModel->BaseConfigModel inheritance...")
    model_gen.fix_models_inheritance()
    logger.info("Models generated and fixed.")

    # 4. Если флаг --django передан, вызываем Django-генератор
    if args.django:
        logger.info("Django mode enabled. Generating Django-specific client code...")
        generate_django_code(swagger_dict, service_dir)
    else:
        # 5. Иначе используем старую логику генерации клиентских классов и фасада
        logger.info("Using legacy client generation.")
        logger.info("Extracting endpoints and imports from swagger.")
        processor = SwaggerProcessor(swagger_dict)
        endpoints = processor.extract_endpoints()
        imports = processor.extract_imports()
        logger.info(f"Found {len(endpoints)} endpoints and {len(imports)} imports.")

        logger.info("Generating client classes (by swagger tags)...")
        client_gen = ClientGenerator(
            endpoints=endpoints,
            imports=imports,
            template_name="client_template.j2"
        )
        file_to_class = client_gen.generate_clients(endpoints_dir, service_name)
        logger.info(f"Generated {len(file_to_class)} client files.")

        logger.info(f"Running auto-format (autoflake, black) on '{service_dir}'...")
        model_gen.post_process_code(service_dir)
        logger.info("Auto-format completed.")

        logger.info("Generating local facade...")
        facade_gen = FacadeGenerator(
            facade_class_name=f"{service_name.capitalize()}Api",
            template_name="facade_template.j2"
        )
        facade_filename = "facade.py"
        facade_gen.generate_facade(file_to_class, service_dir, facade_filename)
        logger.info("Local facade generated successfully.")

        logger.info("Generating global facade (api_facade.py)...")
        generate_app_facade(
            template_name="app_facade.j2",
            output_path="http_clients/api_facade.py",
            base_dir="http_clients"
        )
        logger.info("Global facade generated successfully.")

    logger.info(
        f"Clients (endpoints/*.py), models, and facade for service '{service_name}' have been created at '{service_dir}'."
    )


if __name__ == "__main__":
    main()
