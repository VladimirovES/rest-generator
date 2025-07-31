"""Базовый абстрактный класс для всех генераторов значений."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseGenerator(ABC):

    @abstractmethod
    def can_handle(self, field_type: Any, field_name: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def generate(
            self,
            field_type: Any,
            field_name: Optional[str] = None,
            current_depth: int = 0,
            max_depth: int = 5,
    ) -> Any:
        pass
