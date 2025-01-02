import json
from typing import Dict, Any

class SwaggerLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.swagger: Dict[str, Any] = {}

    def load(self) -> None:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.swagger = json.load(f)

    def get_swagger_dict(self) -> Dict[str, Any]:
        return self.swagger

    def get_service_name(self) -> str:
        info = self.swagger.get("info", {})
        title = info.get("title", "default")
        return title.strip().lower().replace(' ', '_')
