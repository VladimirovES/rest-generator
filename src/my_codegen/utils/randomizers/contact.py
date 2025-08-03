class ContactRandomizers:
    @staticmethod
    def email(domain: Optional[str] = None) -> str:
        """Генерация случайного email адреса"""
        domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'test.com', 'example.org']
        selected_domain = domain or random.choice(domains)
        username = BasicRandomizers.string(random.randint(5, 12), string.ascii_lowercase + string.digits)
        return f"{username}@{selected_domain}"

    @staticmethod
    def phone(country_code: str = "+7") -> str:
        """Генерация случайного номера телефона"""
        if country_code == "+7":  # Россия
            return f"+7{random.randint(900, 999)}{random.randint(1000000, 9999999)}"
        elif country_code == "+1":  # США
            area = random.randint(200, 999)
            exchange = random.randint(200, 999)
            number = random.randint(1000, 9999)
            return f"+1{area}{exchange}{number}"
        else:
            return f"{country_code}{random.randint(1000000000, 9999999999)}"