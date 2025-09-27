"""Model generator for creating Pydantic models from OpenAPI specifications."""

import os
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

from utils.shell import run_command


class IModelGenerator(ABC):
    """Interface for model generators."""

    @abstractmethod
    def generate_models(self) -> None:
        """Generate models from specification."""
        pass

    @abstractmethod
    def post_process_code(self, output_dir: str) -> None:
        """Post-process generated code."""
        pass


class ModelGenerator(IModelGenerator):
    """Generates Pydantic models from OpenAPI/Swagger specifications."""

    # Class constants
    DEFAULT_PYTHON_VERSION = "3.9"
    DEFAULT_MODEL_TYPE = "pydantic_v2.BaseModel"
    MODELS_FILE_EXTENSION = ".py"
    def __init__(self, swagger_path: str, models_file: str = "models") -> None:
        """Initialize the model generator.

        Args:
            swagger_path: Path to the OpenAPI/Swagger specification file
            models_file: Base name for the models file (without extension)

        Raises:
            ValueError: If swagger_path is empty or models_file is invalid
            FileNotFoundError: If swagger_path doesn't exist
        """
        if not swagger_path.strip():
            raise ValueError("swagger_path cannot be empty")
        if not models_file.strip():
            raise ValueError("models_file cannot be empty")

        swagger_file = Path(swagger_path)
        if not swagger_file.exists():
            raise FileNotFoundError(f"Swagger file not found: {swagger_path}")

        self._swagger_path = swagger_path
        self._models_file = models_file
        self._models_path = f"{models_file}{self.MODELS_FILE_EXTENSION}"

    def generate_models(self) -> None:
        """Generate Pydantic models from OpenAPI specification.

        Raises:
            RuntimeError: If model generation fails
        """
        try:
            cmd_parts = self._build_generation_command()
            run_command(" ".join(cmd_parts))
            self._fix_root_models()
        except Exception as e:
            raise RuntimeError(f"Model generation failed: {e}") from e

    def _build_generation_command(self) -> List[str]:
        """Build the datamodel-codegen command."""
        return [
            "datamodel-codegen",
            f"--input {self._swagger_path}",
            "--input-file-type openapi",
            f"--output {self._models_path}",
            "--reuse-model",
            "--use-title-as-name",
            "--use-schema-description",
            "--collapse-root-models",
            "--disable-appending-item-suffix",
            f"--target-python-version {self.DEFAULT_PYTHON_VERSION}",
            f"--output-model-type {self.DEFAULT_MODEL_TYPE}",
            "--use-annotated",
        ]

    def _fix_root_models(self) -> None:
        """Replace simple RootModel with type aliases.

        This method converts RootModel classes to more readable type aliases
        when the RootModel only contains a single annotated field.
        """
        models_file = Path(self._models_path)
        if not models_file.exists():
            return

        try:
            content = models_file.read_text(encoding="utf-8")
            original_content = content

            content = self._replace_root_models(content)

            if content != original_content and "RootModel" not in content:
                content = self._remove_rootmodel_import(content)

            models_file.write_text(content, encoding="utf-8")
        except IOError as e:
            raise RuntimeError(f"Failed to fix root models: {e}") from e

    def _replace_root_models(self, content: str) -> str:
        """Replace RootModel patterns with type aliases."""
        pattern = (
            r"class (\w+)\(RootModel\[([^\]]+)\]\):\s*\n\s*root: (Annotated\[[^\]]+\])"
        )

        def replacement(match):
            class_name = match.group(1)
            annotated_type = match.group(3)
            return f"{class_name} = {annotated_type}"

        return re.sub(pattern, replacement, content)

    def _remove_rootmodel_import(self, content: str) -> str:
        """Remove RootModel import from file."""
        lines = content.split("\n")
        processed_lines = []

        for line in lines:
            if line.strip().startswith("from pydantic import"):
                cleaned_line = self._clean_rootmodel_from_import(line)
                if cleaned_line:
                    processed_lines.append(cleaned_line)
            else:
                processed_lines.append(line)

        return "\n".join(processed_lines)

    def _clean_rootmodel_from_import(self, line: str) -> Optional[str]:
        """Remove RootModel from pydantic import line.

        Args:
            line: The import line to clean

        Returns:
            The cleaned import line, or None if the line should be removed
        """
        prefix = "from pydantic import "
        if not line.strip().startswith(prefix):
            return line

        after_import = line.strip()[len(prefix):]
        imports_list = [imp.strip() for imp in after_import.split(",")]
        filtered_imports = [imp for imp in imports_list if imp != "RootModel"]

        if not filtered_imports:
            return None  # Remove entire line if no imports left

        return f"{prefix}{', '.join(filtered_imports)}"

    def fix_models_inheritance(self) -> None:
        """Replace BaseModel with BaseConfigModel and fix imports.

        Raises:
            RuntimeError: If inheritance fixing fails
        """
        models_file = Path(self._models_path)
        if not models_file.exists():
            return

        try:
            lines = self._read_file()
            lines = self._replace_base_model(lines)
            lines = self._fix_pydantic_imports(lines)
            lines = self._add_config_import_if_needed(lines)

            models_file.write_text("".join(lines), encoding="utf-8")
        except IOError as e:
            raise RuntimeError(f"Failed to fix model inheritance: {e}") from e

    def _read_file(self) -> List[str]:
        """Read models file.

        Returns:
            List of lines from the models file

        Raises:
            IOError: If file cannot be read
        """
        try:
            return Path(self._models_path).read_text(encoding="utf-8").splitlines(keepends=True)
        except IOError as e:
            raise IOError(f"Failed to read models file: {e}") from e

    def _replace_base_model(self, lines: List[str]) -> List[str]:
        """Replace BaseModel with BaseConfigModel"""
        base_model_pattern = re.compile(r"\bBaseModel\b")
        return [base_model_pattern.sub("BaseConfigModel", line) for line in lines]

    def _fix_pydantic_imports(self, lines: List[str]) -> List[str]:
        """Remove BaseModel from pydantic imports"""
        new_lines = []

        for line in lines:
            if line.strip().startswith("from pydantic import"):
                cleaned_line = self._clean_pydantic_import(line)
                if cleaned_line:
                    new_lines.append(cleaned_line)
            else:
                new_lines.append(line)

        return new_lines

    def _clean_pydantic_import(self, line: str) -> str:
        """Remove BaseModel from pydantic import line"""
        prefix = "from pydantic import "
        after_import = line.strip()[len(prefix) :]

        imports_list = [imp.strip() for imp in after_import.split(",")]
        filtered_imports = [
            imp for imp in imports_list if imp not in ("BaseModel", "BaseConfigModel")
        ]

        if not filtered_imports:
            return ""

        return f"{prefix}{', '.join(filtered_imports)}\n"

    def _add_config_import_if_needed(self, lines: List[str]) -> List[str]:
        """Add BaseConfigModel import if it's missing"""
        config_import = (
            "from pydantic_utils.pydantic_config import BaseConfigModel\n"
        )

        if any("BaseConfigModel" in line and "import" in line for line in lines):
            return lines

        last_import_index = self._find_last_import_index(lines)

        if last_import_index >= 0:
            lines.insert(last_import_index + 1, config_import)
        else:
            lines.insert(0, config_import)

        return lines

    def _find_last_import_index(self, lines: List[str]) -> int:
        """Find index of last import line"""
        last_import_index = -1
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                last_import_index = idx
        return last_import_index

    def post_process_code(self, output_dir: str) -> None:
        """Remove unused imports and format code.

        Args:
            output_dir: Directory containing generated code to post-process

        Raises:
            ValueError: If output_dir is invalid
        """
        if not output_dir.strip():
            raise ValueError("output_dir cannot be empty")

        output_path = Path(output_dir)
        if not output_path.exists():
            raise ValueError(f"Output directory does not exist: {output_dir}")

        try:
            self._remove_unused_imports(output_dir)
            self._format_code(output_dir)
        except Exception as e:
            # Log warning but don't fail the entire process
            print(f"Warning: Code post-processing failed: {e}")
            print("Generated code may not be formatted, but functionality is preserved.")

    def _remove_unused_imports(self, output_dir: str) -> None:
        """Remove unused imports with autoflake."""
        cmd_parts = [
            "autoflake",
            "--remove-all-unused-imports",
            "--recursive",
            "--in-place",
            f"'{output_dir}'",
        ]
        run_command(" ".join(cmd_parts))

    def _format_code(self, output_dir: str) -> None:
        """Format code with black."""
        run_command(f"black '{output_dir}'")
