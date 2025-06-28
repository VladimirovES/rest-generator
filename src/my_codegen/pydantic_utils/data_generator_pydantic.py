"""
Главный модуль для генерации данных Pydantic моделей.
Сохраняет обратную совместимость с существующим кодом.
"""

from typing import Any
from faker import Faker
from my_codegen.pydantic_utils.pydantic_config import BaseConfigModel

from my_codegen.pydantic_utils.generators.type_utils import TypeUtils 
from my_codegen.pydantic_utils.generators.value_generator import ValueGenerator, RandomValueGenerator 


fake = Faker()
__all__ = ['GenerateData', 'RandomValueGenerator', 'fake']


class GenerateData:
    """Генератор данных для Pydantic моделей"""

    def __init__(self, model_class: type[BaseConfigModel], current_depth: int = 0,
                 max_depth: int = 5, use_smart_generation: bool = True):
        self.model_class = model_class
        self.data = {}
        self.current_depth = current_depth
        self.max_depth = max_depth
        self.use_smart_generation = use_smart_generation

    def _fill_fields(self, required_only: bool = False, optional_only: bool = False):
        """Заполняет поля модели"""
        fields = self.model_class.model_fields

        for field_name, field_info in fields.items():
            if field_name in self.data:
                continue

            annotation = field_info.annotation
            is_optional = TypeUtils.is_optional(annotation)

            if required_only and is_optional:
                continue
            if optional_only and not is_optional:
                continue

            real_type = TypeUtils.extract_base_type(annotation) if is_optional else annotation

            # Генерируем значение с учетом имени поля (если включена умная генерация)
            field_name_for_gen = field_name if self.use_smart_generation else None
            self.data[field_name] = ValueGenerator.generate(
                real_type, field_name_for_gen, self.current_depth, self.max_depth
            )

    def fill_all_fields(self, **data):
        self.data.update(data)
        self._fill_fields(required_only=False, optional_only=False)
        return self

    def fill_required(self, **data):
        self.data.update(data)
        self._fill_fields(required_only=True, optional_only=False)
        return self

    def fill_optional(self, **data):
        self.data.update(data)
        self._fill_fields(required_only=False, optional_only=True)
        return self

    def set_field(self, **kwargs):
        self.data.update(kwargs)
        return self

    def build(self):
        return self.model_class.model_construct(_validate=False, **self.data)

    def to_dict(self):
        return self._convert_to_dict(self.build())

    def _convert_to_dict(self, instance: BaseConfigModel):
        if isinstance(instance, BaseConfigModel):
            result = {}
            for k, v in instance.__dict__.items():
                if isinstance(v, BaseConfigModel):
                    result[k] = self._convert_to_dict(v)
                elif isinstance(v, list):
                    result[k] = [self._convert_to_dict(i) for i in v]
                elif isinstance(v, dict):
                    result[k] = {kk: self._convert_to_dict(vv) for kk, vv in v.items()}
                else:
                    result[k] = v
            return result
        return instance