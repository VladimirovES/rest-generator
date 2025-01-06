from typing import Optional

from http_clients.cde.facade import CdeApi


class ApiFacade:

    cde: "CdeApi"

    def __init__(self, auth_token: Optional[str] = None):
        self.auth_token = auth_token
        self._instances = {}

    def __getattr__(self, name: str):
        if name not in self._instances:
            self._instances[name] = self._initialize_api(name)
        return self._instances[name]

    def _initialize_api(self, name: str):
        api_classes = {
            "cde": CdeApi,
        }
        if name in api_classes:
            return api_classes[name](self.auth_token)
        else:
            raise AttributeError(f"No such API facade: {name}")