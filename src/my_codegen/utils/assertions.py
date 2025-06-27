import re
from typing import Any, Union
from datetime import datetime, date, timedelta

from my_codegen.utils.report_utils import Reporter
from my_codegen.utils.logger import logger


class Expect:

    def __init__(self, actual: Any, name: str):
        self.actual = actual
        self._name = name
        self._negated = False

    def _not(self) -> 'Expect':
        new_expect = Expect(self.actual, self._name)
        new_expect._negated = not self._negated
        return new_expect

    def _format_value(self, value: Any, max_length: int = 200) -> str:
        """Форматирует значение для отображения в ошибках"""
        if isinstance(value, str):
            if len(value) > max_length:
                return f"'{value[:max_length]}...'"
            return f"'{value}'"
        elif isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, (list, tuple)):
            if len(value) == 0:
                return "[]"
            # Для коллекций объектов показываем краткую информацию
            if hasattr(value[0], '__class__') and hasattr(value[0], '__dict__'):
                # Это объект, показываем только тип и количество
                class_name = value[0].__class__.__name__
                return f"[{len(value)} {class_name} objects]"
            elif len(str(value)) > max_length:
                return f"[{len(value)} items] First 3: {list(value)[:3]}"
            return str(value)
        elif isinstance(value, dict):
            if len(str(value)) > max_length:
                keys = list(value.keys())[:3]
                return f"{{dict with {len(value)} keys}} Sample keys: {keys}"
            return str(value)
        elif hasattr(value, '__class__') and hasattr(value, '__dict__'):
            # Это пользовательский объект
            class_name = value.__class__.__name__
            if hasattr(value, 'id'):
                return f"{class_name}(id={getattr(value, 'id')})"
            return f"{class_name} object"
        else:
            return repr(value)

    def _fail(self, message: str, expected: Any = None):
        negation = "NOT " if self._negated else ""

        # Убираем дублирование - если message уже содержит имя, не добавляем его снова
        if self._name in message:
            full_message = message
        else:
            full_message = f"{self._name} expected {negation}{message}"

        if expected is not None:
            full_message += f"\n\nExpected: {expected}"

        full_message += f"\nActual: {self._format_value(self.actual)}"

        raise AssertionError(full_message)

    def _success(self, message: str):
        """Логирует успешную проверку"""
        success_message = f'"{self._name}" {message}'

    def _check(self, condition: bool, message: str, expected: Any = None):
        message_step = f'Check: "{self._name}" {message}'

        logger.info(f"{message_step}")
        with Reporter.step(f"{message_step}"):

            if self._negated:
                condition = not condition

            if not condition:
                self._fail(message, expected)
            else:
                self._success(f"{message}")

        return self

    # ===============================
    # БАЗОВЫЕ ПРОВЕРКИ (для всех типов)
    # ===============================

    def is_equal(self, expected: Any) -> 'Expect':
        return self._check(
            self.actual == expected,
            f"to equal {self._format_value(expected)}",
            self._format_value(expected)
        )

    def is_not_equal(self, expected: Any) -> 'Expect':
        return self._check(
            self.actual != expected,
            f"to not equal {self._format_value(expected)}",
            f"anything except {self._format_value(expected)}"
        )

    def is_none(self) -> 'Expect':
        return self._check(
            self.actual is None,
            "to be None",
            "None"
        )

    def is_not_none(self) -> 'Expect':
        return self._check(
            self.actual is not None,
            "to not be None",
            "any non-None value"
        )

    def is_greater_than(self, expected: Union[int, float]) -> 'Expect':
        return self._check(
            self.actual > expected,
            f"to be greater than {expected}",
            f"value > {expected} (actual: {self.actual})"
        )

    def is_less_than(self, expected: Union[int, float]) -> 'Expect':
        return self._check(
            self.actual < expected,
            f"to be less than {expected}",
            f"value < {expected} (actual: {self.actual})"
        )

    def is_greater_than_or_equal(self, expected: Union[int, float]) -> 'Expect':
        return self._check(
            self.actual >= expected,
            f"to be greater than or equal to {expected}",
            f"value >= {expected} (actual: {self.actual})"
        )

    def is_less_than_or_equal(self, expected: Union[int, float]) -> 'Expect':
        return self._check(
            self.actual <= expected,
            f"to be less than or equal to {expected}",
            f"value <= {expected} (actual: {self.actual})"
        )

    def contains(self, substring: str) -> 'Expect':
        if not isinstance(self.actual, str):
            self._fail(f"to be a string for contains check, but got {type(self.actual).__name__}")

        contains = substring in self.actual
        if not contains:
            preview = self.actual[:100] + "..." if len(self.actual) > 100 else self.actual
            return self._check(
                False,
                f"to contain '{substring}'",
                f"string containing '{substring}' (actual string: '{preview}')"
            )

        return self._check(contains, f"to contain '{substring}'")

    def starts_with(self, prefix: str) -> 'Expect':
        if not isinstance(self.actual, str):
            self._fail(f"to be a string for starts_with check, but got {type(self.actual).__name__}")
        return self._check(
            self.actual.startswith(prefix),
            f"to start with '{prefix}'",
            f"string starting with '{prefix}' (actual: {self._format_value(self.actual)})"
        )

    def ends_with(self, suffix: str) -> 'Expect':
        if not isinstance(self.actual, str):
            self._fail(f"to be a string for ends_with check, but got {type(self.actual).__name__}")
        return self._check(
            self.actual.endswith(suffix),
            f"to end with '{suffix}'",
            f"string ending with '{suffix}' (actual: {self._format_value(self.actual)})"
        )

    def matches(self, pattern: str) -> 'Expect':
        if not isinstance(self.actual, str):
            self._fail(f"to be a string for regex match, but got {type(self.actual).__name__}")

        matches = re.search(pattern, self.actual) is not None
        return self._check(
            matches,
            f"to match pattern '{pattern}'",
            f"string matching pattern '{pattern}' (actual: {self._format_value(self.actual)})"
        )

    # ===============================
    #       ПРОВЕРКИ КОЛЛЕКЦИЙ
    # ===============================

    def has_length(self, expected_length: int) -> 'Expect':
        try:
            actual_length = len(self.actual)
        except TypeError:
            self._fail("to have length (no len() method)")

        return self._check(
            actual_length == expected_length,
            f"to have length {expected_length}",
            f"length {expected_length} (actual length: {actual_length})"
        )

    def is_empty(self) -> 'Expect':
        try:
            actual_length = len(self.actual)
            return self._check(
                actual_length == 0,
                "to be empty",
                f"empty collection (actual length: {actual_length})"
            )
        except TypeError:
            self._fail("to be empty (no len() method)")

    def is_not_empty(self) -> 'Expect':
        try:
            actual_length = len(self.actual)
            return self._check(
                actual_length > 0,
                "to not be empty",
                f"non-empty collection (actual length: {actual_length})"
            )
        except TypeError:
            self._fail("to check emptiness (no len() method)")

    def contains_item(self, item: Any) -> 'Expect':
        try:
            contains = item in self.actual
            if not contains:
                if hasattr(self.actual, '__len__') and len(self.actual) <= 10:
                    available_items = f"Available items: {list(self.actual)}"
                elif hasattr(self.actual, '__len__'):
                    available_items = f"Collection has {len(self.actual)} items. First 5: {list(self.actual)[:5]}"
                else:
                    available_items = "Unknown collection content"

                return self._check(
                    False,
                    f"to contain item {self._format_value(item)}",
                    f"collection containing {self._format_value(item)}. {available_items}"
                )

            return self._check(contains, f"to contain item {self._format_value(item)}")
        except TypeError:
            self._fail("to be iterable for item check")

    def contains_items(self, *items: Any) -> 'Expect':
        for item in items:
            self.contains_item(item)
        return self

    def is_sorted_asc(self, key_func=None) -> 'Expect':
        if not hasattr(self.actual, '__iter__') or isinstance(self.actual, str):
            self._fail("to be iterable for sorting check")

        items = list(self.actual)
        if len(items) <= 1:
            return self._check(True, "to be sorted asc (trivially true for 0-1 items)")

        if key_func:
            values = [key_func(item) for item in items]
            message = f"to be sorted asc by key function"
        else:
            values = items
            message = "to be sorted asc"

        is_sorted = all(values[i] <= values[i + 1] for i in range(len(values) - 1))

        if not is_sorted:
            # Находим первое нарушение
            violation_idx = next((i for i in range(len(values) - 1) if values[i] > values[i + 1]), None)
            violation_info = f"violation at index {violation_idx}: {values[violation_idx]} > {values[violation_idx + 1]}"
            preview = values[:10] + ["..."] if len(values) > 10 else values

            return self._check(
                False,
                message,
                f"asc sorted sequence. {violation_info}. Preview: {preview}"
            )

        return self._check(is_sorted, message)

    def is_sorted_descending(self, key_func=None) -> 'Expect':
        if not hasattr(self.actual, '__iter__') or isinstance(self.actual, str):
            self._fail("to be iterable for sorting check")

        items = list(self.actual)
        if len(items) <= 1:
            return self._check(True, "to be sorted descending (trivially true for 0-1 items)")

        if key_func:
            values = [key_func(item) for item in items]
            message = f"to be sorted descending by key function"
        else:
            values = items
            message = "to be sorted descending"

        is_sorted = all(values[i] >= values[i + 1] for i in range(len(values) - 1))

        if not is_sorted:
            violation_idx = next((i for i in range(len(values) - 1) if values[i] < values[i + 1]), None)
            violation_info = f"violation at index {violation_idx}: {values[violation_idx]} < {values[violation_idx + 1]}"
            preview = values[:10] + ["..."] if len(values) > 10 else values

            return self._check(
                False,
                message,
                f"descending sorted sequence. {violation_info}. Preview: {preview}"
            )

        return self._check(is_sorted, message)

    def is_sorted_by_field(self, field_name: str, asc: bool = True) -> 'Expect':
        if not hasattr(self.actual, '__iter__') or isinstance(self.actual, str):
            self._fail("to be iterable for field sorting check")

        items = list(self.actual)
        if len(items) <= 1:
            direction = "asc" if asc else "descending"
            return self._check(True, f"to be sorted by field '{field_name}' {direction} (trivially true for 0-1 items)")

        try:
            values = []
            for i, item in enumerate(items):
                if hasattr(item, field_name):
                    values.append(getattr(item, field_name))
                elif isinstance(item, dict) and field_name in item:
                    values.append(item[field_name])
                else:
                    self._fail(f"to have field '{field_name}' accessible in all items (failed at item {i})")

            if asc:
                is_sorted = all(values[i] <= values[i + 1] for i in range(len(values) - 1))
                direction = "asc"
                comparison = ">"
            else:
                is_sorted = all(values[i] >= values[i + 1] for i in range(len(values) - 1))
                direction = "descending"
                comparison = "<"

            if not is_sorted:
                # Находим первое нарушение порядка
                violation_idx = None
                for i in range(len(values) - 1):
                    if asc and values[i] > values[i + 1]:
                        violation_idx = i
                        break
                    elif not asc and values[i] < values[i + 1]:
                        violation_idx = i
                        break

                if violation_idx is not None:
                    # Форматируем значения в зависимости от типа
                    val1 = self._format_value(values[violation_idx])
                    val2 = self._format_value(values[violation_idx + 1])

                    violation_info = f"violation at index {violation_idx}: {val1} {comparison} {val2}"

                    # Показываем превью значений поля (не полных объектов)
                    preview_values = []
                    for v in values[:10]:
                        preview_values.append(self._format_value(v))
                    if len(values) > 10:
                        preview_values.append("...")

                    expected_text = f"field '{field_name}' in {direction} order. {violation_info}. Field values: {preview_values}"

                    return self._check(
                        False,
                        f"to be sorted by field '{field_name}' {direction}",
                        expected_text
                    )

            return self._check(is_sorted, f"to be sorted by field '{field_name}' {direction}")

        except Exception as e:
            self._fail(f"to be sortable by field '{field_name}': {str(e)}")

    def has_unique_values(self, key_func=None) -> 'Expect':
        if not hasattr(self.actual, '__iter__') or isinstance(self.actual, str):
            self._fail("to be iterable for uniqueness check")

        items = list(self.actual)

        if key_func:
            values = [key_func(item) for item in items]
            message = "to have unique values by key function"
        else:
            values = items
            message = "to have unique values"

        unique_values = set(values)
        is_unique = len(values) == len(unique_values)

        if not is_unique:
            # Найдем дубликаты
            seen = set()
            duplicates = []
            for value in values:
                if value in seen and value not in duplicates:
                    duplicates.append(value)
                seen.add(value)

            return self._check(
                False,
                message,
                f"all unique values (found {len(duplicates)} duplicates: {duplicates[:5]}{'...' if len(duplicates) > 5 else ''})"
            )

        return self._check(is_unique, message)

    def has_unique_values_by(self, field_name: str) -> 'Expect':
        return self.has_unique_values(lambda item:
                                    getattr(item, field_name) if hasattr(item, field_name)
                                    else item.get(field_name) if isinstance(item, dict)
                                    else None
                                    )

    # ===============================
    #          ПРОВЕРКА ДАТЫ
    # ===============================

    def _parse_date(self, value: Any) -> datetime:
        """Парсер дат - только основные форматы"""
        if isinstance(value, datetime):
            return value
        elif isinstance(value, date):
            return datetime.combine(value, datetime.min.time())
        elif isinstance(value, str):
            formats = [
                "%Y-%m-%d",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO format with microseconds
                "%Y-%m-%dT%H:%M:%SZ",  # ISO format without microseconds
                "%d.%m.%Y"
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
            self._fail(f"to be a valid date string, but got '{value}'")
        else:
            self._fail(f"to be a date, but got {type(value).__name__}")

    def is_after(self, date_threshold: Union[datetime, date, str]) -> 'Expect':
        actual_dt = self._parse_date(self.actual)
        threshold_dt = self._parse_date(date_threshold)
        return self._check(
            actual_dt > threshold_dt,
            f"to be after {threshold_dt.strftime('%Y-%m-%d %H:%M:%S')}",
            f"date after {threshold_dt.strftime('%Y-%m-%d %H:%M:%S')} (actual: {actual_dt.strftime('%Y-%m-%d %H:%M:%S')})"
        )

    def is_before(self, date_threshold: Union[datetime, date, str]) -> 'Expect':
        actual_dt = self._parse_date(self.actual)
        threshold_dt = self._parse_date(date_threshold)
        return self._check(
            actual_dt < threshold_dt,
            f"to be before {threshold_dt.strftime('%Y-%m-%d %H:%M:%S')}",
            f"date before {threshold_dt.strftime('%Y-%m-%d %H:%M:%S')} (actual: {actual_dt.strftime('%Y-%m-%d %H:%M:%S')})"
        )

    def is_today(self) -> 'Expect':
        actual_dt = self._parse_date(self.actual)
        today = date.today()
        return self._check(
            actual_dt.date() == today,
            f"to be today ({today})",
            f"today's date ({today}) (actual: {actual_dt.date()})"
        )

    def is_around_now(self, minutes: int = 1) -> 'Expect':
        actual_dt = self._parse_date(self.actual)
        now = datetime.now()
        delta = timedelta(minutes=minutes)
        min_time = now - delta
        max_time = now + delta

        is_around = min_time <= actual_dt <= max_time
        return self._check(
            is_around,
            f"to be around now (±{minutes} minutes)",
            f"time between {min_time.strftime('%H:%M:%S')} and {max_time.strftime('%H:%M:%S')} (actual: {actual_dt.strftime('%H:%M:%S')})"
        )

    def is_close_to_now(self, seconds: int = 60) -> 'Expect':
        actual_dt = self._parse_date(self.actual)
        now = datetime.now()
        delta = timedelta(seconds=seconds)
        min_time = now - delta
        max_time = now + delta

        is_close = min_time <= actual_dt <= max_time
        return self._check(
            is_close,
            f"to be close to now (±{seconds} seconds)",
            f"time between {min_time.strftime('%H:%M:%S')} and {max_time.strftime('%H:%M:%S')} (actual: {actual_dt.strftime('%H:%M:%S')})"
        )

    def is_just_created(self, tolerance_minutes: int = 2) -> 'Expect':
        actual_dt = self._parse_date(self.actual)
        now = datetime.now()
        min_time = now - timedelta(minutes=tolerance_minutes)

        is_just_created = min_time <= actual_dt <= now
        return self._check(
            is_just_created,
            f"to be just created (within last {tolerance_minutes} minutes)",
            f"creation time between {min_time.strftime('%H:%M:%S')} and {now.strftime('%H:%M:%S')} (actual: {actual_dt.strftime('%H:%M:%S')})"
        )

    def is_recently_updated(self, minutes_ago: int = 5) -> 'Expect':
        actual_dt = self._parse_date(self.actual)
        now = datetime.now()
        threshold = now - timedelta(minutes=minutes_ago)

        is_recent = actual_dt >= threshold
        return self._check(
            is_recent,
            f"to be recently updated (within last {minutes_ago} minutes)",
            f"update time after {threshold.strftime('%H:%M:%S')} (actual: {actual_dt.strftime('%H:%M:%S')})"
        )


# ===============================
# ПРОСТОЙ API - ОДНА ФУНКЦИЯ
# ===============================

def expect(actual: Any, name: str) -> Expect:
    return Expect(actual, name)