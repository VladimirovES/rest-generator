import os
import re
from typing import List
from my_codegen.utils.shell import run_command


class ModelGenerator:
    def __init__(self, swagger_path: str, models_file: str = "models"):
        self.swagger_path = swagger_path
        self.models_file = models_file
        self.models_path = f"{models_file}.py"

    def generate_models(self) -> None:
        """Generate Pydantic models from Swagger via datamodel-codegen"""
        cmd_parts = [
            "datamodel-codegen",
            f"--input {self.swagger_path}",
            "--input-file-type openapi",
            f"--output {self.models_path}",
            "--reuse-model",
            "--use-title-as-name",
            "--use-schema-description",
            "--collapse-root-models",
            "--disable-appending-item-suffix",
            "--target-python-version 3.9",
            "--output-model-type pydantic_v2.BaseModel",
            "--use-annotated",
        ]
        run_command(" ".join(cmd_parts))
        self._fix_root_models()

    def _fix_root_models(self) -> None:
        """Replace simple RootModel with type aliases"""
        if not os.path.exists(self.models_path):
            return

        with open(self.models_path, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = (
            r"class (\w+)\(RootModel\[([^\]]+)\]\):\s*\n\s*root: (Annotated\[[^\]]+\])"
        )

        def replacement(match):
            class_name = match.group(1)
            annotated_type = match.group(3)
            return f"{class_name} = {annotated_type}"

        original_content = content
        content = re.sub(pattern, replacement, content)

        if content != original_content and "RootModel" not in content:
            content = self._remove_rootmodel_import(content)

        with open(self.models_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _remove_rootmodel_import(self, content: str) -> str:
        """Remove RootModel import from file"""
        lines = content.split("\n")
        new_lines = []

        for line in lines:
            if line.strip().startswith("from pydantic import"):
                cleaned_line = self._clean_rootmodel_from_import(line)
                if cleaned_line:
                    new_lines.append(cleaned_line)
            else:
                new_lines.append(line)

        return "\n".join(new_lines)

    def _clean_rootmodel_from_import(self, line: str) -> str:
        """Remove RootModel from pydantic import line"""
        prefix = "from pydantic import "
        if not line.strip().startswith(prefix):
            return line

        after_import = line.strip()[len(prefix) :]
        imports_list = [imp.strip() for imp in after_import.split(",")]
        filtered_imports = [imp for imp in imports_list if imp != "RootModel"]

        if not filtered_imports:
            return ""  # Remove entire line if no imports left

        return f"{prefix}{', '.join(filtered_imports)}"

    def fix_models_inheritance(self) -> None:
        """Replace BaseModel with BaseConfigModel and fix imports"""
        if not os.path.exists(self.models_path):
            return

        lines = self._read_file()
        lines = self._replace_base_model(lines)
        lines = self._fix_pydantic_imports(lines)
        lines = self._add_config_import_if_needed(lines)

        with open(self.models_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def _read_file(self) -> List[str]:
        """Read models file"""
        with open(self.models_path, "r", encoding="utf-8") as f:
            return f.readlines()

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
            "from my_codegen.pydantic_utils.pydantic_config import BaseConfigModel\n"
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
        """Remove unused imports and format code"""
        try:
            # Remove unused imports with autoflake
            cmd_parts = [
                "autoflake",
                "--remove-all-unused-imports",
                "--recursive",
                "--in-place",
                f"'{output_dir}'",
            ]
            run_command(" ".join(cmd_parts))

            # Format code with black
            run_command(f"black '{output_dir}'")
        except Exception as e:
            # Log warning but don't fail the entire process
            print(f"Warning: Code formatting failed: {e}")
            print("Generated code may not be formatted, but functionality is preserved.")
