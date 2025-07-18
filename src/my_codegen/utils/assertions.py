import re
from typing import Any, Union, Optional, Callable, List
from datetime import datetime, date, timedelta

from my_codegen.utils.report_utils import Reporter
from my_codegen.utils.logger import logger


class Expect:
    """Класс для проверок."""

    MAX_STRING_LENGTH = 200
    MAX_COLLECTION_PREVIEW = 5
    MAX_DICT_KEYS_PREVIEW = 3

    def __init__(self, actual: Any, name: str):
        self.actual = actual
        self._name = name
        self._negated = False

    def _not(self) -> "Expect":
        """Создает инвертированную проверку."""
        new_expect = Expect(self.actual, self._name)
        new_expect._negated = not self._negated
        return new_expect

    def _format_value(self, value: Any, max_length: int = MAX_STRING_LENGTH) -> str:
        """
        Форматирует значение для отображения в ошибках.
        Делает вывод более читаемым и информативным.
        """
        if value is None:
            return "None"

        if isinstance(value, str):
            if len(value) > max_length:
                return (
                    f"'{value[:max_length]}...' (обрезано, полная длина: {len(value)})"
                )
            return f"'{value}'"

        elif isinstance(value, bool):
            return str(value)

        elif isinstance(value, (int, float)):
            return str(value)

        elif isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")

        elif isinstance(value, date):
            return value.strftime("%Y-%m-%d")

        elif isinstance(value, (list, tuple)):
            return self._format_collection(value, max_length)

        elif isinstance(value, dict):
            return self._format_dict(value, max_length)

        elif isinstance(value, set):
            return self._format_set(value, max_length)

        elif hasattr(value, "__class__") and hasattr(value, "__dict__"):
            return self._format_object(value)

        else:
            result = repr(value)
            if len(result) > max_length:
                return f"{result[:max_length]}... (обрезано)"
            return result

    def _format_collection(self, value: Union[List, tuple], max_length: int) -> str:
        """Форматирует список или кортеж."""
        if len(value) == 0:
            return "[]" if isinstance(value, list) else "()"

        # Для коллекций объектов
        if value and hasattr(value[0], "__class__") and hasattr(value[0], "__dict__"):
            class_name = value[0].__class__.__name__
            return f"[{len(value)} объектов типа {class_name}]"

        # Для простых коллекций
        if len(value) <= self.MAX_COLLECTION_PREVIEW:
            formatted_items = [self._format_value(item, 50) for item in value]
            return f"[{', '.join(formatted_items)}]"
        else:
            preview_items = [self._format_value(item, 50) for item in value[:3]]
            return f"[{', '.join(preview_items)}, ... всего {len(value)} элементов]"

    def _format_dict(self, value: dict, max_length: int) -> str:
        """Форматирует словарь."""
        if not value:
            return "{}"

        if len(str(value)) <= max_length and len(value) <= 5:
            return str(value)

        keys = list(value.keys())[: self.MAX_DICT_KEYS_PREVIEW]
        key_preview = ", ".join(f"'{k}'" for k in keys)
        return f"{{словарь с {len(value)} ключами: {key_preview}, ...}}"

    def _format_set(self, value: set, max_length: int) -> str:
        """Форматирует множество."""
        if not value:
            return "set()"

        if len(value) <= self.MAX_COLLECTION_PREVIEW:
            items = [self._format_value(item, 50) for item in value]
            return f"{{{', '.join(items)}}}"
        else:
            items = list(value)[:3]
            preview = [self._format_value(item, 50) for item in items]
            return f"{{{', '.join(preview)}, ... всего {len(value)} элементов}}"

    def _format_object(self, value: Any) -> str:
        """Форматирует пользовательский объект."""
        class_name = value.__class__.__name__

        # Попытка получить идентификатор объекта
        identifiers = []
        for attr in ["id", "name", "title", "code"]:
            if hasattr(value, attr):
                attr_value = getattr(value, attr)
                if attr_value is not None:
                    identifiers.append(f"{attr}={self._format_value(attr_value, 30)}")

        if identifiers:
            return f"{class_name}({', '.join(identifiers[:2])})"
        return f"{class_name} объект"

    def _create_error_message(
        self,
        expectation: str,
        actual_formatted: str,
        expected_formatted: Optional[str] = None,
        additional_info: Optional[str] = None,
    ) -> str:
        """
        Создает понятное сообщение об ошибке.
        """
        lines = []

        negation = "НЕ " if self._negated else ""
        lines.append(f'CheckName -  "{self._name}"')

        if expected_formatted:
            lines.append(f"Expected: {expected_formatted}")

        lines.append(f"Actual: {actual_formatted}")

        if additional_info:
            lines.append(f"Additional info: {additional_info}")

        return "\n".join(lines)

    def _fail(
        self, expectation: str, expected: Any = None, additional_info: str = None
    ):
        """Генерирует понятное сообщение об ошибке и выбрасывает исключение."""
        actual_formatted = self._format_value(self.actual)
        expected_formatted = (
            self._format_value(expected) if expected is not None else None
        )

        message = self._create_error_message(
            expectation, actual_formatted, expected_formatted, additional_info
        )

        raise AssertionError(message)

    def _success(self, message: str):
        """Логирует успешную проверку."""
        success_message = f'✓ "{self._name}" {message}'
        logger.debug(success_message)

    def _check(
        self,
        condition: bool,
        expectation: str,
        expected: Any = None,
        additional_info: str = None,
    ) -> "Expect":
        """Выполняет проверку с логированием."""
        message_step = f'Проверка: "{self._name}" {expectation}'

        with Reporter.step(message_step):
            if self._negated:
                condition = not condition

            if not condition:
                self._fail(expectation, expected, additional_info)
            else:
                self._success(expectation)

        return self

    # ===============================
    # БАЗОВЫЕ ПРОВЕРКИ
    # ===============================

    def is_equal(self, expected: Any) -> "Expect":
        """Проверяет точное равенство значений."""
        return self._check(
            self.actual == expected,
            f"должно быть равно {self._format_value(expected)}",
            expected,
        )

    def is_not_equal(self, expected: Any) -> "Expect":
        """Проверяет неравенство значений."""
        return self._check(
            self.actual != expected,
            f"не должно быть равно {self._format_value(expected)}",
            f"любое значение кроме {self._format_value(expected)}",
        )

    def is_none(self) -> "Expect":
        """Проверяет, что значение None."""
        return self._check(self.actual is None, "должно быть None", "None")

    def is_not_none(self) -> "Expect":
        """Проверяет, что значение не None."""
        return self._check(
            self.actual is not None, "не должно быть None", "любое значение кроме None"
        )

    def is_greater_than(self, expected: Union[int, float]) -> "Expect":
        """Проверяет, что значение больше ожидаемого."""
        return self._check(
            self.actual > expected,
            f"должно быть больше {expected}",
            f"значение > {expected}",
        )

    def is_less_than(self, expected: Union[int, float]) -> "Expect":
        """Проверяет, что значение меньше ожидаемого."""
        return self._check(
            self.actual < expected,
            f"должно быть меньше {expected}",
            f"значение < {expected}",
        )

    def is_greater_than_or_equal(self, expected: Union[int, float]) -> "Expect":
        """Проверяет, что значение больше или равно ожидаемому."""
        return self._check(
            self.actual >= expected,
            f"должно быть больше или равно {expected}",
            f"значение >= {expected}",
        )

    def is_less_than_or_equal(self, expected: Union[int, float]) -> "Expect":
        """Проверяет, что значение меньше или равно ожидаемому."""
        return self._check(
            self.actual <= expected,
            f"должно быть меньше или равно {expected}",
            f"значение <= {expected}",
        )

    # ===============================
    # СТРОКОВЫЕ ПРОВЕРКИ
    # ===============================

    def contains(self, substring: str) -> "Expect":
        """Проверяет, что строка содержит подстроку."""
        if not isinstance(self.actual, str):
            self._fail(
                f"должно быть строкой для проверки contains",
                "строка",
                f"получен тип {type(self.actual).__name__}",
            )

        if substring not in self.actual:
            # Показываем контекст вокруг похожих частей
            preview = (
                self.actual[:100] + "..." if len(self.actual) > 100 else self.actual
            )
            return self._check(
                False,
                f"должно содержать '{substring}'",
                f"строка, содержащая '{substring}'",
                f"В строке '{preview}' подстрока не найдена",
            )

        return self._check(True, f"должно содержать '{substring}'")

    def matches(self, pattern: str) -> "Expect":
        """Проверяет соответствие строки регулярному выражению."""
        if not isinstance(self.actual, str):
            self._fail(
                "должно быть строкой для проверки regex",
                "строка",
                f"получен тип {type(self.actual).__name__}",
            )

        matches = re.search(pattern, self.actual) is not None
        return self._check(
            matches,
            f"должно соответствовать паттерну '{pattern}'",
            f"строка, соответствующая паттерну '{pattern}'",
        )

    # ===============================
    # ПРОВЕРКИ КОЛЛЕКЦИЙ
    # ===============================

    def has_length(self, expected_length: int) -> "Expect":
        """Проверяет длину коллекции."""
        try:
            actual_length = len(self.actual)
        except TypeError:
            self._fail(
                "должно иметь длину",
                f"объект с длиной {expected_length}",
                "объект не поддерживает len()",
            )

        return self._check(
            actual_length == expected_length,
            f"должно иметь длину {expected_length}",
            f"длина {expected_length}",
            f"Фактическая длина: {actual_length}",
        )

    def is_empty(self) -> "Expect":
        """Проверяет, что коллекция пуста."""
        try:
            actual_length = len(self.actual)
            return self._check(
                actual_length == 0,
                "должно быть пустым",
                "пустая коллекция",
                f"Коллекция содержит {actual_length} элементов",
            )
        except TypeError:
            self._fail(
                "должно быть коллекцией для проверки пустоты",
                "коллекция",
                "объект не поддерживает len()",
            )

    def is_not_empty(self) -> "Expect":
        """Проверяет, что коллекция не пуста."""
        try:
            actual_length = len(self.actual)
            return self._check(
                actual_length > 0, "не должно быть пустым", "непустая коллекция"
            )
        except TypeError:
            self._fail(
                "должно быть коллекцией", "коллекция", "объект не поддерживает len()"
            )

    def contains_item(self, item: Any) -> "Expect":
        """Проверяет наличие элемента в коллекции."""
        try:
            if item not in self.actual:
                # Формируем подсказку о доступных элементах
                if hasattr(self.actual, "__len__"):
                    length = len(self.actual)
                    if length == 0:
                        hint = "Коллекция пуста"
                    elif length <= 10:
                        hint = f"Доступные элементы: {list(self.actual)}"
                    else:
                        first_items = list(self.actual)[:5]
                        hint = f"Всего {length} элементов. Первые 5: {first_items}"
                else:
                    hint = "Содержимое коллекции неизвестно"

                return self._check(
                    False,
                    f"должно содержать элемент {self._format_value(item)}",
                    f"коллекция с элементом {self._format_value(item)}",
                    hint,
                )

            return self._check(
                True, f"должно содержать элемент {self._format_value(item)}"
            )

        except TypeError:
            self._fail(
                "должно быть итерируемым",
                "итерируемый объект",
                f"получен тип {type(self.actual).__name__}",
            )

    def contains_items(self, *items: Any) -> "Expect":
        """Проверяет наличие нескольких элементов в коллекции."""
        for item in items:
            self.contains_item(item)
        return self

    def is_sorted_asc(self, key_func: Optional[Callable] = None) -> "Expect":
        """Проверяет сортировку по возрастанию."""
        return self._check_sorting(ascending=True, key_func=key_func)

    def is_sorted_descending(self, key_func: Optional[Callable] = None) -> "Expect":
        """Проверяет сортировку по убыванию."""
        return self._check_sorting(ascending=False, key_func=key_func)

    def _check_sorting(
        self, ascending: bool, key_func: Optional[Callable] = None
    ) -> "Expect":
        """Общий метод проверки сортировки."""
        if not hasattr(self.actual, "__iter__") or isinstance(self.actual, str):
            self._fail(
                "должно быть итерируемым для проверки сортировки",
                "итерируемый объект",
                f"получен тип {type(self.actual).__name__}",
            )

        items = list(self.actual)
        if len(items) <= 1:
            direction = "по возрастанию" if ascending else "по убыванию"
            return self._check(
                True,
                f"должно быть отсортировано {direction} (тривиально для 0-1 элементов)",
            )

        # Получаем значения для сравнения
        if key_func:
            try:
                values = [key_func(item) for item in items]
                key_info = " (с использованием key функции)"
            except Exception as e:
                self._fail(
                    "key функция должна работать для всех элементов",
                    "корректная key функция",
                    f"Ошибка: {str(e)}",
                )
        else:
            values = items
            key_info = ""

        # Проверяем сортировку
        direction = "по возрастанию" if ascending else "по убыванию"

        for i in range(len(values) - 1):
            if ascending and values[i] > values[i + 1]:
                is_sorted = False
                break
            elif not ascending and values[i] < values[i + 1]:
                is_sorted = False
                break
        else:
            is_sorted = True

        if not is_sorted:
            # Находим место нарушения
            comparison = ">" if ascending else "<"
            val1 = self._format_value(values[i], 50)
            val2 = self._format_value(values[i + 1], 50)

            preview = [self._format_value(v, 30) for v in values[:10]]
            if len(values) > 10:
                preview.append("...")

            return self._check(
                False,
                f"должно быть отсортировано {direction}{key_info}",
                f"отсортированная {direction} последовательность",
                f"Нарушение на позиции {i}: {val1} {comparison} {val2}. Значения: {preview}",
            )

        return self._check(
            is_sorted, f"должно быть отсортировано {direction}{key_info}"
        )

    def is_sorted_by_field(self, field_name: str, asc: bool = True) -> "Expect":
        """Проверяет сортировку по полю объекта."""

        def get_field_value(item):
            if hasattr(item, field_name):
                return getattr(item, field_name)
            elif isinstance(item, dict) and field_name in item:
                return item[field_name]
            else:
                raise AttributeError(f"Поле '{field_name}' не найдено")

        direction = "по возрастанию" if asc else "по убыванию"

        try:
            return self._check_sorting(ascending=asc, key_func=get_field_value)
        except AttributeError as e:
            self._fail(
                f"все элементы должны иметь поле '{field_name}'",
                f"объекты с полем '{field_name}'",
                str(e),
            )

    # ===============================
    # ПРОВЕРКИ ДАТЫ И ВРЕМЕНИ
    # ===============================

    def _parse_date(self, value: Any) -> datetime:
        """Парсит дату из различных форматов."""
        if isinstance(value, datetime):
            return value
        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        elif isinstance(value, str):
            # Пробуем различные форматы
            formats = [
                "%Y-%m-%d",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S",
                "%d.%m.%Y",
                "%d.%m.%Y %H:%M:%S",
                "%d/%m/%Y",
                "%d/%m/%Y %H:%M:%S",
            ]

            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue

            # Если ни один формат не подошел
            self._fail(
                "должно быть валидной датой",
                "дата в одном из поддерживаемых форматов",
                f"Строка '{value}' не распознана как дата. Поддерживаемые форматы: YYYY-MM-DD, DD.MM.YYYY и др.",
            )
        else:
            self._fail(
                "должно быть датой",
                "datetime, date или строка с датой",
                f"получен тип {type(value).__name__}",
            )

    def is_after(self, date_threshold: Union[datetime, date, str]) -> "Expect":
        """Проверяет, что дата после указанной."""
        actual_dt = self._parse_date(self.actual)
        threshold_dt = self._parse_date(date_threshold)

        return self._check(
            actual_dt > threshold_dt,
            f"должно быть после {threshold_dt.strftime('%Y-%m-%d %H:%M:%S')}",
            f"дата после {threshold_dt.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Разница: {actual_dt - threshold_dt}",
        )

    def is_before(self, date_threshold: Union[datetime, date, str]) -> "Expect":
        """Проверяет, что дата до указанной."""
        actual_dt = self._parse_date(self.actual)
        threshold_dt = self._parse_date(date_threshold)

        return self._check(
            actual_dt < threshold_dt,
            f"должно быть до {threshold_dt.strftime('%Y-%m-%d %H:%M:%S')}",
            f"дата до {threshold_dt.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Разница: {threshold_dt - actual_dt}",
        )

    def is_today(self) -> "Expect":
        """Проверяет, что дата - сегодня."""
        actual_dt = self._parse_date(self.actual)
        today = date.today()

        return self._check(
            actual_dt.date() == today,
            f"должно быть сегодняшней датой ({today})",
            f"дата {today}",
            f"Дата {actual_dt.date()}",
        )

    def is_around_now(self, minutes: int = 1) -> "Expect":
        """Проверяет, что время близко к текущему (±минуты)."""
        actual_dt = self._parse_date(self.actual)
        now = datetime.now()
        delta = timedelta(minutes=minutes)
        min_time = now - delta
        max_time = now + delta

        is_around = min_time <= actual_dt <= max_time

        time_diff = abs((actual_dt - now).total_seconds())
        diff_str = (
            f"{time_diff:.1f} секунд"
            if time_diff < 60
            else f"{time_diff / 60:.1f} минут"
        )

        return self._check(
            is_around,
            f"должно быть около текущего времени (±{minutes} мин)",
            f"время между {min_time.strftime('%H:%M:%S')} и {max_time.strftime('%H:%M:%S')}",
            f"Разница с текущим временем: {diff_str}",
        )

    def is_close_to_now(self, seconds: int = 60) -> "Expect":
        """Проверяет, что время близко к текущему (±секунды)."""
        actual_dt = self._parse_date(self.actual)
        now = datetime.now()
        delta = timedelta(seconds=seconds)
        min_time = now - delta
        max_time = now + delta

        is_close = min_time <= actual_dt <= max_time

        time_diff = abs((actual_dt - now).total_seconds())

        return self._check(
            is_close,
            f"должно быть близко к текущему времени (±{seconds} сек)",
            f"время между {min_time.strftime('%H:%M:%S')} и {max_time.strftime('%H:%M:%S')}",
            f"Разница: {time_diff:.1f} секунд",
        )

    def is_just_created(self, tolerance_minutes: int = 2) -> "Expect":
        """Проверяет, что объект только что создан."""
        actual_dt = self._parse_date(self.actual)
        now = datetime.now()
        min_time = now - timedelta(minutes=tolerance_minutes)

        is_just_created = min_time <= actual_dt <= now

        if actual_dt > now:
            additional = "Время создания в будущем!"
        else:
            time_ago = (now - actual_dt).total_seconds() / 60
            additional = f"Создано {time_ago:.1f} минут назад"

        return self._check(
            is_just_created,
            f"должно быть только что создано (в пределах {tolerance_minutes} мин)",
            f"время создания между {min_time.strftime('%H:%M:%S')} и {now.strftime('%H:%M:%S')}",
            additional,
        )


# ===============================
# API
# ===============================


def expect(actual: Any, name: str) -> Expect:
    """
    Создает объект для проверки значения.

    Args:
        actual: Проверяемое значение
        name: Описательное имя для значения (используется в сообщениях об ошибках)

    Returns:
        Expect: Объект с методами проверки

    Example:
        expect(user.age, "Возраст пользователя").is_greater_than(18)
        expect(items, "Список товаров").is_not_empty().has_length(5)
    """
    return Expect(actual, name)
