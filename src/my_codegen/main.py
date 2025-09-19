import os
import sys
from typing import Tuple
import click

from dotenv import load_dotenv

from my_codegen.codegen.facade_generator import FacadeGenerator
from my_codegen.codegen.generate_app_facade import generate_app_facade
from my_codegen.codegen.client_generator import ClientGenerator
from my_codegen.codegen.model_generator import ModelGenerator
from my_codegen.swagger.loader import SwaggerLoader
from my_codegen.swagger.processor import SwaggerProcessor
from my_codegen.utils.logger import logger
from my_codegen.constants import (
    DEFAULT_SWAGGER_PATH,
    DEFAULT_OUTPUT_DIR,
    FACADE_FILENAME,
    APP_FACADE_FILENAME,
    CLIENT_TEMPLATE,
    FACADE_TEMPLATE,
    APP_FACADE_TEMPLATE,
)

load_dotenv()


class RestGenError(Exception):
    """Base exception for rest generator"""
    pass


class SwaggerProcessingError(RestGenError):
    """Error during swagger processing"""
    pass


class CodeGenerationError(RestGenError):
    """Error during code generation"""
    pass


class RestGenerator:
    """Main generator class that orchestrates the entire process"""

    def __init__(self, swagger_url: str, output_dir: str = DEFAULT_OUTPUT_DIR):
        self.swagger_url = swagger_url
        self.output_dir = output_dir
        self.swagger_path = DEFAULT_SWAGGER_PATH

    def generate(self) -> None:
        """Main generation workflow"""
        try:
            # Step 1: Download and load swagger
            swagger_spec, module_name, service_path = self._load_swagger()

            # Step 2: Setup directories
            service_dir, endpoints_dir = self._setup_directories(module_name)

            # Step 3: Generate models
            self._generate_models(service_dir)

            # Step 4: Process swagger and generate clients
            file_to_class = self._generate_clients(
                swagger_spec, module_name, service_path, endpoints_dir
            )

            # Step 5: Post-process code
            self._post_process_code(service_dir)

            # Step 6: Generate facades
            self._generate_facades(module_name, service_dir, file_to_class)

            logger.info(
                f"Successfully generated clients, models, and facades for service "
                f"'{module_name}' at '{service_dir}'"
            )

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise RestGenError(f"Failed to generate REST client: {e}") from e

    def _load_swagger(self) -> Tuple[object, str, str]:
        """Download and load swagger specification"""
        try:
            logger.info("Downloading Swagger file...")
            loader = SwaggerLoader(self.swagger_path)
            loader.download_swagger(url=self.swagger_url)

            logger.info("Parsing Swagger specification...")
            loader.load()

            swagger_spec = loader.swagger_spec
            module_name = loader.get_module_name()
            service_path = loader.get_service_path()

            logger.info(f"Service identified as: {module_name}")
            return swagger_spec, module_name, service_path

        except Exception as e:
            raise SwaggerProcessingError(f"Failed to load swagger: {e}") from e

    def _setup_directories(self, module_name: str) -> Tuple[str, str]:
        """Create necessary output directories"""
        try:
            service_dir = os.path.join(self.output_dir, module_name)
            endpoints_dir = os.path.join(service_dir, "endpoints")

            os.makedirs(service_dir, exist_ok=True)
            os.makedirs(endpoints_dir, exist_ok=True)

            logger.info(f"Created directories: '{service_dir}' and '{endpoints_dir}'")
            return service_dir, endpoints_dir

        except OSError as e:
            raise CodeGenerationError(f"Failed to create directories: {e}") from e

    def _generate_models(self, service_dir: str) -> None:
        """Generate Pydantic models"""
        try:
            logger.info("Generating Pydantic models...")
            models_file = os.path.join(service_dir, "models")
            model_gen = ModelGenerator(self.swagger_path, models_file)

            model_gen.generate_models()
            logger.info("Models generated. Fixing inheritance...")
            model_gen.fix_models_inheritance()
            logger.info("Model inheritance fixed.")

        except Exception as e:
            raise CodeGenerationError(f"Failed to generate models: {e}") from e

    def _generate_clients(
        self, swagger_spec: object, module_name: str, service_path: str, endpoints_dir: str
    ) -> dict:
        """Generate client classes"""
        try:
            logger.info("Extracting endpoints and imports from swagger...")
            processor = SwaggerProcessor(swagger_spec)
            endpoints = processor.extract_endpoints()
            imports = processor.extract_imports()

            logger.info(f"Found {len(endpoints)} endpoints and {len(imports)} imports")

            logger.info("Generating client classes...")
            client_gen = ClientGenerator(
                endpoints=endpoints, imports=imports, template_name=CLIENT_TEMPLATE
            )
            file_to_class = client_gen.generate_clients(
                endpoints_dir, module_name, service_path
            )

            logger.info(f"Generated {len(file_to_class)} client files")
            return file_to_class

        except Exception as e:
            raise CodeGenerationError(f"Failed to generate clients: {e}") from e

    def _post_process_code(self, service_dir: str) -> None:
        """Run code formatting and cleanup"""
        try:
            logger.info("Running code formatting...")
            # Use the model generator's post-processing method
            # This could be refactored to a separate utility class
            model_gen = ModelGenerator("", "")  # Temporary instance
            model_gen.post_process_code(service_dir)
            logger.info("Code formatting completed")

        except Exception as e:
            logger.warning(f"Code formatting failed: {e}")
            # Don't fail the entire process for formatting issues

    def _generate_facades(self, module_name: str, service_dir: str, file_to_class: dict) -> None:
        """Generate local and global facades"""
        try:
            # Generate local facade
            logger.info("Generating local facade...")
            facade_class_name = self._generate_facade_class_name(module_name)
            facade_gen = FacadeGenerator(
                facade_class_name=facade_class_name, template_name=FACADE_TEMPLATE
            )
            facade_gen.generate_facade(file_to_class, service_dir, FACADE_FILENAME)
            logger.info("Local facade generated")

            # Generate global facade
            logger.info("Generating global facade...")
            app_facade_path = os.path.join(self.output_dir, APP_FACADE_FILENAME)
            generate_app_facade(
                template_name=APP_FACADE_TEMPLATE,
                output_path=app_facade_path,
                base_dir=self.output_dir,
            )
            logger.info("Global facade generated")

        except Exception as e:
            raise CodeGenerationError(f"Failed to generate facades: {e}") from e

    @staticmethod
    def _generate_facade_class_name(module_name: str) -> str:
        """Generate facade class name from module name"""
        return "".join(word.capitalize() for word in module_name.split("_")) + "Api"


@click.command()
@click.option(
    "--swagger-url",
    required=True,
    help="URL to download the Swagger JSON from"
)
@click.option(
    "--output-dir",
    default=DEFAULT_OUTPUT_DIR,
    help=f"Output directory for generated files (default: {DEFAULT_OUTPUT_DIR})"
)
def main(swagger_url: str, output_dir: str) -> None:
    """Generate REST API client from Swagger/OpenAPI specification"""
    try:
        generator = RestGenerator(swagger_url, output_dir)
        generator.generate()
    except RestGenError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
