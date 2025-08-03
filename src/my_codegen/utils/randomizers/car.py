class CarRandomizers:
    @staticmethod
    def brand() -> str:
        """Генерация случайной марки автомобиля"""
        brands = [
            "Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "Hyundai", "Kia",
            "Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Lexus", "Mazda",
            "Subaru", "Volvo", "Jeep", "Dodge", "Chrysler", "Buick", "Cadillac",
            "Lada", "УАЗ", "ГАЗ", "Камаз", "Москвич"
        ]
        return random.choice(brands)

    @staticmethod
    def model() -> str:
        """Генерация случайной модели автомобиля"""
        models = [
            "Camry", "Corolla", "Civic", "Accord", "F-150", "Silverado",
            "Altima", "Sentra", "Elantra", "Sonata", "Optima", "Sorento",
            "Jetta", "Passat", "Golf", "3 Series", "5 Series", "C-Class",
            "E-Class", "A3", "A4", "Q5", "CX-5", "Mazda3", "Outback",
            "Forester", "XC60", "XC90", "Cherokee", "Grand Cherokee",
            "Granta", "Vesta", "Patriot", "Hunter", "Газель", "Соболь"
        ]
        return random.choice(models)

    @staticmethod
    def year() -> int:
        """Генерация случайного года выпуска автомобиля"""
        current_year = datetime.datetime.now().year
        return random.randint(1990, current_year + 1)

    @staticmethod
    def vin_number() -> str:
        """Генерация случайного VIN номера"""
        chars = string.ascii_uppercase + string.digits
        chars = chars.replace('I', '').replace('O', '').replace('Q', '')
        return ''.join(random.choices(chars, k=17))

    @staticmethod
    def license_plate(region: str = "RU") -> str:
        """Генерация случайного номерного знака"""
        if region == "RU":
            letters = "АВЕКМНОРСТУХ"
            letter1 = random.choice(letters)
            numbers = f"{random.randint(100, 999)}"
            letter2 = random.choice(letters)
            letter3 = random.choice(letters)
            region_code = f"{random.randint(10, 99)}"
            return f"{letter1}{numbers}{letter2}{letter3}{region_code}"
        elif region == "US":
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            numbers = f"{random.randint(1000, 9999)}"
            return f"{letters}-{numbers}"
        else:
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

    @staticmethod
    def color() -> str:
        """Генерация случайного цвета автомобиля"""
        colors = [
            "Белый", "Черный", "Серый", "Серебристый", "Красный", "Синий",
            "Зеленый", "Желтый", "Оранжевый", "Коричневый", "Фиолетовый",
            "Бежевый", "Золотистый", "Бордовый", "Темно-синий", "Металлик"
        ]
        return random.choice(colors)

    @staticmethod
    def engine_volume() -> float:
        """Генерация случайного объема двигателя в литрах"""
        volumes = [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.5, 2.7, 3.0, 3.5, 4.0, 5.0]
        return random.choice(volumes)

    @staticmethod
    def fuel_type() -> str:
        """Генерация случайного типа топлива"""
        fuel_types = ["Бензин", "Дизель", "Гибрид", "Электро", "ГБО", "Бензин+ГБО"]
        return random.choice(fuel_types)

    @staticmethod
    def transmission() -> str:
        """Генерация случайного типа трансмиссии"""
        transmissions = ["МКПП", "АКПП", "Вариатор", "Робот"]
        return random.choice(transmissions)

    @staticmethod
    def mileage() -> int:
        """Генерация случайного пробега в километрах"""
        return random.randint(0, 500000)

    @staticmethod
    def full_data() -> Dict[str, Any]:
        """Генерация полных данных об автомобиле"""
        return {
            "brand": CarRandomizers.brand(),
            "model": CarRandomizers.model(),
            "year": CarRandomizers.year(),
            "color": CarRandomizers.color(),
            "vin": CarRandomizers.vin_number(),
            "license_plate": CarRandomizers.license_plate(),
            "engine_volume": CarRandomizers.engine_volume(),
            "fuel_type": CarRandomizers.fuel_type(),
            "transmission": CarRandomizers.transmission(),
            "mileage": CarRandomizers.mileage(),
            "price": BasicRandomizers.integer(100000, 5000000)
        }
