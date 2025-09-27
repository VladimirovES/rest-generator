import os
import sys
from typing import Tuple
import click

from dotenv import load_dotenv

from codegen.facade_generator import FacadeGenerator
from codegen.generate_app_facade import generate_app_facade
from codegen.enhanced_client_generator import EnhancedClientGenerator
from codegen.tests_generator import TestsGenerator
from swagger.loader import SwaggerLoader
from swagger.processor import SwaggerProcessor
from utils.logger import logger
from exceptions import (
    RestGeneratorError,
    SwaggerProcessingError,
    CodeGenerationError,
)
from constants import (
    DEFAULT_SWAGGER_PATH,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_TESTS_DIR,
    FACADE_FILENAME,
    APP_FACADE_FILENAME,
    CLIENT_TEMPLATE,
    FACADE_TEMPLATE,
    APP_FACADE_TEMPLATE,
)

load_dotenv()




class RestGenerator:
    """Main generator class that orchestrates the REST client generation process.

    This class handles the complete workflow from Swagger/OpenAPI specification
    processing to generating Python client code, models, and facades.

    Args:
        swagger_url: URL to the Swagger/OpenAPI specification
        output_dir: Directory where generated code will be saved
    """

    def __init__(
        self,
        swagger_url: str,
        output_dir: str = DEFAULT_OUTPUT_DIR,
        generate_tests: bool = False,
    ):
        self.swagger_url = swagger_url
        self.output_dir = output_dir
        self.swagger_path = DEFAULT_SWAGGER_PATH
        self.generate_tests = generate_tests

    def generate(self) -> None:
        """Main generation workflow"""
        try:
            # Step 1: Download and load swagger
            swagger_spec, module_name, service_path = self._load_swagger()

            # Step 2: Setup directories
            service_dir = self._setup_directories(module_name)

            # Step 3: Generate clients with models
            (
                file_to_class,
                module_endpoints,
                model_definitions,
            ) = self._generate_clients_with_models(swagger_spec, service_dir)

            # Step 4: Generate test skeletons (optional)
            if self.generate_tests:
                self._generate_tests_structure(
                    module_name,
                    file_to_class,
                    module_endpoints,
                    model_definitions,
                )

            # Step 5: Post-process code
            self._post_process_code(service_dir)

            # Step 6: Generate facades
            self._generate_facades(module_name, service_dir, file_to_class)

            # Step 7: Copy base modules
            self._copy_base_modules(self.output_dir)

            logger.info(
                f"Successfully generated clients, models, and facades for service "
                f"'{module_name}' at '{service_dir}'"
            )

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise RestGeneratorError(f"Failed to generate REST client: {e}") from e

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

    def _setup_directories(self, module_name: str) -> str:
        """Create necessary output directories"""
        try:
            service_dir = os.path.join(self.output_dir, module_name)
            os.makedirs(service_dir, exist_ok=True)

            logger.info(f"Created service directory: '{service_dir}'")
            return service_dir

        except OSError as e:
            raise CodeGenerationError(f"Failed to create directories: {e}") from e


    def _generate_clients_with_models(
        self, swagger_spec: object, service_dir: str
    ) -> Tuple[dict, dict, dict]:
        """Generate client classes with models per endpoint"""
        try:
            logger.info("Extracting endpoints and imports from swagger...")
            processor = SwaggerProcessor(swagger_spec)
            endpoints = processor.extract_endpoints()
            imports = processor.extract_imports()

            logger.info(f"Found {len(endpoints)} endpoints and {len(imports)} imports")

            logger.info("Generating client classes with models...")
            # Convert swagger_spec to dict for model generator
            import json
            with open(self.swagger_path, 'r', encoding='utf-8') as f:
                swagger_dict = json.load(f)

            client_gen = EnhancedClientGenerator(
                endpoints=endpoints,
                imports=imports,
                template_name=CLIENT_TEMPLATE,
                openapi_spec=swagger_dict
            )
            file_to_class = client_gen.generate_clients_with_models(service_dir)
            module_endpoints = client_gen.get_module_endpoints()
            model_definitions = client_gen.get_model_definitions()

            logger.info(f"Generated {len(file_to_class)} client files with models")
            return file_to_class, module_endpoints, model_definitions

        except Exception as e:
            raise CodeGenerationError(f"Failed to generate clients with models: {e}") from e

    def _post_process_code(self, service_dir: str) -> None:
        """Run code formatting and cleanup"""
        try:
            logger.info("Running code formatting...")
            from utils.shell import run_command

            # Run autoflake to remove unused imports
            run_command(f"autoflake --remove-all-unused-imports --recursive --in-place {service_dir}")

            # Run black to format code
            run_command(f"black {service_dir}")

            logger.info("Code formatting completed")

        except Exception as e:
            logger.warning(f"Code formatting failed: {e}")
            # Don't fail the entire process for formatting issues

    def _generate_tests_structure(
        self,
        module_name: str,
        file_to_class: dict,
        module_endpoints: dict,
        model_definitions: dict,
    ) -> None:
        """Create placeholder tests mirroring the client structure."""
        if not file_to_class:
            logger.info("No clients generated; skipping test skeleton creation")
            return

        try:
            tests_root, package_root = self._resolve_tests_root()
            tests_generator = TestsGenerator(
                tests_root, package_root, model_definitions
            )
            tests_generator.generate(
                module_name, file_to_class, module_endpoints
            )
            service_tests_dir = os.path.join(tests_root, module_name)
            logger.info(
                f"Generated placeholder tests for service '{module_name}' at '{service_tests_dir}'"
            )
        except Exception as e:
            logger.warning(f"Failed to generate test skeletons: {e}")

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

    def _copy_base_modules(self, output_dir: str) -> None:
        """Copy base modules (rest_client, exceptions) to output directory"""
        try:
            import shutil
            import os

            logger.info("Copying base modules...")

            # Get the source directory (where this script is located)
            src_dir = os.path.dirname(os.path.abspath(__file__))

            # Copy rest_client module
            rest_client_src = os.path.join(src_dir, "rest_client")
            rest_client_dst = os.path.join(output_dir, "rest_client")
            if os.path.exists(rest_client_dst):
                shutil.rmtree(rest_client_dst)
            shutil.copytree(rest_client_src, rest_client_dst)

            # Copy exceptions module
            exceptions_src = os.path.join(src_dir, "exceptions.py")
            exceptions_dst = os.path.join(output_dir, "exceptions.py")
            shutil.copy2(exceptions_src, exceptions_dst)

            logger.info("Base modules copied successfully")

        except Exception as e:
            logger.warning(f"Failed to copy base modules: {e}")
            # Don't fail the entire process for this

    @staticmethod
    def _generate_facade_class_name(module_name: str) -> str:
        """Generate facade class name from module name"""
        return "".join(word.capitalize() for word in module_name.split("_")) + "Facade"

    def _resolve_tests_root(self) -> Tuple[str, str]:
        """Resolve tests root directory and corresponding client package name."""
        output_abs = os.path.abspath(self.output_dir)
        normalized_output = output_abs.rstrip(os.sep)
        if not normalized_output:
            normalized_output = output_abs

        rest_clients_dirname = os.path.basename(normalized_output) or DEFAULT_OUTPUT_DIR
        parent_dir = os.path.dirname(normalized_output) or os.getcwd()

        tests_parent = os.path.join(parent_dir, DEFAULT_TESTS_DIR)
        os.makedirs(tests_parent, exist_ok=True)

        tests_root = os.path.join(tests_parent, rest_clients_dirname)
        os.makedirs(tests_root, exist_ok=True)

        return tests_root, rest_clients_dirname


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
@click.option(
    "--tests",
    is_flag=True,
    default=False,
    help="Generate placeholder test skeletons alongside clients",
)
def main(swagger_url: str, output_dir: str, tests: bool) -> None:
    """Generate REST API client from Swagger/OpenAPI specification"""
    try:
        generator = RestGenerator(swagger_url, output_dir, generate_tests=tests)
        generator.generate()
    except RestGeneratorError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
