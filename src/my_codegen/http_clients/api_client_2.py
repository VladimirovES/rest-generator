import httpx

from abc import ABC, abstractmethod


class BaseHttpClient(ABC):
    @abstractmethod
    def get(
            self,
            url: str,
            **kwargs: Any
    ) -> dict:
        pass

    def post(self,
             url: str,
             **kwargs: Any
             ) -> dict:
        pass



class HttpClient(BaseHttpClient):
    def get(self,url: str,**kwargs: Any) -> dict:
        return requests.get(url, **kwargs).json()




class ApiClient:
    def __init__(self,http_client: BaseHttpClient):
        self.http_client = http_client

    def get_user(self, user_id, headers) -> dict:
        return self.http_client.get(
            f"{API_URL}/user/{user_id}",
            headers=headers,
        ).json()


