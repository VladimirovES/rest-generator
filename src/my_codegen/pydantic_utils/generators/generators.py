"""Конкретные реализации генераторов для различных типов данных."""

import random
from datetime import datetime, date, timedelta
from typing import (
    Any,
    List,
    Dict,
    Union,
    Set,
    Type,
    Callable,
    Optional,
    get_args,
    get_origin,
    ForwardRef,
    Annotated,
)
from uuid import UUID, uuid4


from faker import Faker
from pydantic import Field, RootModel

from .base_generator import BaseGenerator
from .type_utils import TypeUtils
from .smart_field_config import SmartFieldConfig

fake = Faker()


class SmartFieldGenerator(BaseGenerator):
    """Генератор, использующий имя поля для умной генерации"""

    def can_handle(self, field_type: Any, field_name: Optional[str] = None) -> bool:
        if field_type is not str or not field_name:
            return False

        field_lower = field_name.lower()

        # Проверяем точное совпадение
        if field_lower in SmartFieldConfig.EXACT_MAPPINGS:
            return True

        # Проверяем паттерны
        return any(
            pattern in field_lower for pattern in SmartFieldConfig.PATTERN_MAPPINGS
        )

    def generate(
        self,
        field_type: Any,
        field_name: Optional[str] = None,
        current_depth: int = 0,
        max_depth: int = 5,
    ) -> Any:
        if not field_name:
            return fake.text(max_nb_chars=20)

        field_lower = field_name.lower()

        # Точное совпадение приоритетнее
        if field_lower in SmartFieldConfig.EXACT_MAPPINGS:
            return SmartFieldConfig.EXACT_MAPPINGS[field_lower]()

        # Ищем по паттернам
        for pattern, generator in SmartFieldConfig.PATTERN_MAPPINGS.items():
            if pattern in field_lower:
                return generator()

        return fake.text(max_nb_chars=20)


class PrimitiveGenerator(BaseGenerator):
    """Генератор примитивных типов"""

    GENERATORS = {
        str: lambda: fake.text(max_nb_chars=20),
        int: lambda: random.randint(1, 1000),
        float: lambda: random.uniform(1.0, 100.0),
        bool: lambda: random.choice([True, False]),
        datetime: lambda: (datetime.now() + timedelta(days=1)).isoformat() + "Z",
        date: lambda: (datetime.now() + timedelta(days=1)).date().isoformat(),
        UUID: lambda: uuid4(),
        Any: lambda: random.choice(
            [fake.word(), random.randint(1, 1000), random.uniform(1.0, 100.0)]
        ),
    }

    def can_handle(self, field_type: Any, field_name: Optional[str] = None) -> bool:
        return field_type in self.GENERATORS

    def generate(
        self,
        field_type: Any,
        field_name: Optional[str] = None,
        current_depth: int = 0,
        max_depth: int = 5,
    ) -> Any:
        return self.GENERATORS[field_type]()


class ContainerGenerator(BaseGenerator):
    """Генератор контейнерных типов"""

    def can_handle(self, field_type: Any, field_name: Optional[str] = None) -> bool:
        origin = get_origin(field_type)
        return origin in (list, List, dict, Dict, set, Set)

    def generate(
        self,
        field_type: Any,
        field_name: Optional[str] = None,
        current_depth: int = 0,
        max_depth: int = 5,
    ) -> Any:
        if current_depth >= max_depth:
            return self._empty_container(field_type)

        origin = get_origin(field_type)
        args = get_args(field_type)

        from .value_generator import ValueGenerator

        if origin in (list, List):
            item_type = args[0] if args else str
            return [
                ValueGenerator.generate(item_type, None, current_depth + 1, max_depth)
                for _ in range(random.randint(1, 2))
            ]

        elif origin in (dict, Dict):
            value_type = args[1] if len(args) > 1 else str
            return {
                fake.word(): ValueGenerator.generate(
                    value_type, None, current_depth + 1, max_depth
                )
                for _ in range(random.randint(1, 2))
            }

        elif origin in (set, Set):
            item_type = args[0] if args else str
            return {
                ValueGenerator.generate(item_type, None, current_depth + 1, max_depth)
                for _ in range(random.randint(1, 2))
            }

    def _empty_container(self, field_type: Any) -> Any:
        origin = get_origin(field_type)
        if origin in (list, List):
            return []
        elif origin in (dict, Dict):
            return {}
        elif origin in (set, Set):
            return set()


class EnumGenerator(BaseGenerator):
    """Генератор для Enum типов"""

    def can_handle(self, field_type: Any, field_name: Optional[str] = None) -> bool:
        return TypeUtils.is_enum(field_type)

    def generate(
        self,
        field_type: Any,
        field_name: Optional[str] = None,
        current_depth: int = 0,
        max_depth: int = 5,
    ) -> Any:
        return random.choice(list(field_type))


class PydanticModelGenerator(BaseGenerator):
    """Генератор для Pydantic моделей"""

    def can_handle(self, field_type: Any, field_name: Optional[str] = None) -> bool:
        return TypeUtils.is_pydantic_model(field_type) or TypeUtils.is_root_model(
            field_type
        )

    def generate(
        self,
        field_type: Any,
        field_name: Optional[str] = None,
        current_depth: int = 0,
        max_depth: int = 5,
    ) -> Any:
        if TypeUtils.is_root_model(field_type):
            return self._generate_root_model(field_type, current_depth, max_depth)
        else:
            return self._generate_pydantic_model(field_type, current_depth, max_depth)

    def _generate_root_model(
        self, field_type: Any, current_depth: int, max_depth: int
    ) -> Any:
        from .value_generator import ValueGenerator

        root_annotation = field_type.model_fields["root"].annotation
        generated = ValueGenerator.generate(
            root_annotation, None, current_depth, max_depth
        )
        return field_type.model_construct(root=generated, _fields_set={"root"})

    def _generate_pydantic_model(
        self, field_type: Any, current_depth: int, max_depth: int
    ) -> Any:
        from .data_generator_pydantic import GenerateData

        if current_depth >= max_depth:
            try:
                from_data = GenerateData(field_type, current_depth, max_depth)
                return from_data.fill_required().build()
            except:
                return None

        from_data = GenerateData(field_type, current_depth + 1, max_depth)
        return from_data.fill_all_fields().build()


class AnnotatedGenerator(BaseGenerator):
    """Генератор для Annotated типов"""

    def can_handle(self, field_type: Any, field_name: Optional[str] = None) -> bool:
        return TypeUtils.is_annotated(field_type)

    def generate(
        self,
        field_type: Any,
        field_name: Optional[str] = None,
        current_depth: int = 0,
        max_depth: int = 5,
    ) -> Any:
        args = get_args(field_type)
        base_type = args[0] if args else str
        metadata = args[1:] if len(args) > 1 else ()

        if base_type is str:
            return self._handle_string_constraints(metadata)

        from .value_generator import ValueGenerator

        return ValueGenerator.generate(base_type, field_name, current_depth, max_depth)

    def _handle_string_constraints(self, metadata: tuple) -> str:
        min_len, max_len = 1, 20

        for meta in metadata:
            try:
                if hasattr(meta, "min_length") and meta.min_length is not None:
                    min_len = max(1, int(meta.min_length))
                if hasattr(meta, "max_length") and meta.max_length is not None:
                    max_len = max(1, int(meta.max_length))

                # Если есть constraints, проверяем и их
                if hasattr(meta, "constraints") and meta.constraints:
                    constraints = meta.constraints
                    if (
                        hasattr(constraints, "min_length")
                        and constraints.min_length is not None
                    ):
                        min_len = max(1, int(constraints.min_length))
                    if (
                        hasattr(constraints, "max_length")
                        and constraints.max_length is not None
                    ):
                        max_len = max(1, int(constraints.max_length))
            except (ValueError, TypeError, AttributeError):
                continue

        # Проверяем корректность диапазона
        if min_len > max_len:
            min_len = 1
            max_len = 20

        target_length = random.randint(min_len, max_len)
        return fake.pystr(min_chars=target_length, max_chars=target_length)


class SpecialTypeGenerator(BaseGenerator):
    """Генератор для специальных Pydantic типов"""

    def can_handle(self, field_type: Any, field_name: Optional[str] = None) -> bool:
        if isinstance(field_type, ForwardRef):
            return True

        field_str = str(field_type)
        return "pydantic" in field_str or any(
            keyword in field_str
            for keyword in ["Url", "Email", "Json", "Path", "Secret", "IPv"]
        )

    def generate(
        self,
        field_type: Any,
        field_name: Optional[str] = None,
        current_depth: int = 0,
        max_depth: int = 5,
    ) -> Any:
        if isinstance(field_type, ForwardRef):
            return []

        field_str = str(field_type)
        field_name_str = getattr(field_type, "__name__", field_str)

        type_mappings = {
            "url": fake.url,
            "email": fake.email,
            "json": lambda: {"example": "data"},
            "path": fake.file_path,
            "secret": fake.password,
            "ipv4": fake.ipv4,
            "ipv6": fake.ipv6,
        }

        for key, generator in type_mappings.items():
            if key in field_str.lower() or key in field_name_str.lower():
                return generator()

        if "pydantic" in field_str:
            return fake.word()

        raise ValueError(f"Unsupported field type: {field_type}")
