class NetworkRandomizers:
    @staticmethod
    def url(scheme: str = None, with_params: bool = False) -> str:
        """Генерация случайного URL"""
        schemes = ['http', 'https'] if scheme is None else [scheme]
        domains = ['example.com', 'test.org', 'sample.net', 'demo.io']
        paths = ['api', 'users', 'products', 'orders', 'data']

        selected_scheme = random.choice(schemes)
        domain = random.choice(domains)
        path = '/'.join(random.choices(paths, k=random.randint(1, 3)))

        url = f"{selected_scheme}://{domain}/{path}"

        if with_params:
            params = []
            for _ in range(random.randint(1, 4)):
                key = BasicRandomizers.string(5, string.ascii_lowercase)
                value = BasicRandomizers.string(8)
                params.append(f"{key}={value}")
            url += "?" + "&".join(params)

        return url

    @staticmethod
    def ipv4() -> str:
        """Генерация случайного IPv4 адреса"""
        return ".".join(str(random.randint(1, 255)) for _ in range(4))

    @staticmethod
    def ipv6() -> str:
        """Генерация случайного IPv6 адреса"""
        groups = []
        for _ in range(8):
            group = format(random.randint(0, 65535), '04x')
            groups.append(group)
        return ":".join(groups)

    @staticmethod
    def mac_address() -> str:
        """Генерация случайного MAC адреса"""
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        return ":".join(f"{x:02x}" for x in mac)
