
from typing import Optional
from my_codegen.rest_client.client import ApiClient

from rest_clients.checkpoints.facade import CheckpointsFacade


class ApiFacade:
    def __init__(self, client: ApiClient):
        self.checkpoints = CheckpointsFacade(client)
