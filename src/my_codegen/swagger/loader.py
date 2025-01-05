import json
from typing import Dict, Any

from my_codegen.utils.shell import run_command


class SwaggerLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.swagger: Dict[str, Any] = {}

    def load(self) -> None:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.swagger = json.load(f)

    def get_service_name(self) -> str:
        info = self.swagger.get("info", {})
        title = info.get("title", "default")
        return title.strip().lower().replace(' ', '_')

    def download_swagger(self, url: str):
        swagger_cmd = f"curl {url} -o ./swagger.json"
        run_command(swagger_cmd)
