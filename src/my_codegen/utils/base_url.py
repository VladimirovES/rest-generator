class BaseUrlSingleton:
    _instance = None
    base_url = ""

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def set_base_url(cls, url):
        cls.get_instance().base_url = url

    @classmethod
    def get_base_url(cls):
        url = cls.get_instance().base_url
        return url