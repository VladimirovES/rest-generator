class ConfigUrl:
    BASE_URL = ""

    @classmethod
    def set_base_url(cls, url):
        cls.BASE_URL = url

    @classmethod
    def get_base_url(cls):
        return cls.BASE_URL
