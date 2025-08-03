import random
import string
import uuid
import datetime
from typing import Optional, List, Dict, Any


class BasicRandomizers:
    @staticmethod
    def string(length: int = 10, charset: str = None) -> str:
        """Генерация случайной строки"""
        if charset is None:
            charset = string.ascii_letters + string.digits
        return ''.join(random.choices(charset, k=length))

    @staticmethod
    def integer(min_val: int = 0, max_val: int = 100) -> int:
        """Генерация случайного целого числа"""
        return random.randint(min_val, max_val)

    @staticmethod
    def float_number(min_val: float = 0.0, max_val: float = 100.0, decimals: int = 2) -> float:
        """Генерация случайного числа с плавающей точкой"""
        value = random.uniform(min_val, max_val)
        return round(value, decimals)

    @staticmethod
    def boolean() -> bool:
        """Генерация случайного булевого значения"""
        return random.choice([True, False])


class IdentifierRandomizers:
    @staticmethod
    def uuid(version: int = 4) -> str:
        """Генерация случайного UUID"""
        if version == 4:
            return str(uuid.uuid4())
        elif version == 1:
            return str(uuid.uuid1())
        else:
            return str(uuid.uuid4())

    @staticmethod
    def jwt_token() -> str:
        """Генерация фейкового JWT токена для тестирования"""
        header = BasicRandomizers.string(36, string.ascii_letters + string.digits + "-_")
        payload = BasicRandomizers.string(180, string.ascii_letters + string.digits + "-_")
        signature = BasicRandomizers.string(43, string.ascii_letters + string.digits + "-_")
        return f"{header}.{payload}.{signature}"


class PersonRandomizers:
    @staticmethod
    def name(locale: str = "ru") -> Dict[str, str]:
        """Генерация случайного имени и фамилии"""
        if locale == "ru":
            first_names = ["Александр", "Анна", "Дмитрий", "Елена", "Михаил", "Ольга", "Сергей", "Татьяна"]
            last_names = ["Иванов", "Петров", "Сидоров", "Козлов", "Волков", "Смирнов", "Попов", "Лебедев"]
        else:  # en
            first_names = ["John", "Jane", "Michael", "Sarah", "David", "Lisa", "Robert", "Emily"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

        return {
            "first_name": random.choice(first_names),
            "last_name": random.choice(last_names)
        }

    @staticmethod
    def address() -> Dict[str, str]:
        """Генерация случайного адреса"""
        streets = ["Ленина", "Пушкина", "Гагарина", "Мира", "Советская", "Центральная"]
        cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]

        return {
            "street": f"ул. {random.choice(streets)}, {random.randint(1, 100)}",
            "city": random.choice(cities),
            "postal_code": f"{random.randint(100000, 999999)}",
            "country": "Россия"
        }


class CollectionRandomizers:
    @staticmethod
    def array(item_generator, min_length: int = 1, max_length: int = 5) -> List[Any]:
        """Генерация случайного массива с заданным генератором элементов"""
        length = random.randint(min_length, max_length)
        return [item_generator() for _ in range(length)]

    @staticmethod
    def dict(keys: List[str], value_generators: Dict[str, callable]) -> Dict[str, Any]:
        """Генерация случайного словаря с заданными ключами и генераторами значений"""
        result = {}
        for key in keys:
            if key in value_generators:
                result[key] = value_generators[key]()
            else:
                result[key] = BasicRandomizers.string()
        return result
