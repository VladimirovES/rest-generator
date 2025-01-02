import os
import re
from utils.shell import run_command


class ModelGenerator:
    def __init__(self, swagger_path: str,
                 models_file: str = 'models'):
        self.swagger_path = swagger_path
        self.models_file = models_file

    def generate_models(self) -> None:
        model_cmd = (
            f"datamodel-codegen --input {self.swagger_path} "
            "--input-file-type openapi "
            f"--output {self.models_file}.py "
            "--reuse-model "
            "--use-title-as-name "
            "--use-schema-description "
            "--collapse-root-models "
            "--target-python-version 3.9"
        )
        run_command(model_cmd)

    def fix_models_inheritance(self) -> None:
        if not os.path.exists(self.models_file):
            print(f"[WARN] {self.models_file} not found, skip fix.")
            return
        ...
        print(f"[INFO] Fixed inheritance in {self.models_file}")

    def post_process_code(self, output_dir: str) -> None:
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
