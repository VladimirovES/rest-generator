
from typing import Optional
from rest_client.client import ApiClient

from rest_clients.cde.facade import CdeFacade


class ApiFacade:
    def __init__(self, client: ApiClient):
        self.cde = CdeFacade(client)
