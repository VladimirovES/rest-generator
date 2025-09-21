"""Validation utilities for testing and assertion."""

import re
from typing import Any, Union, Optional, Callable, List, Dict, Set
from datetime import datetime, date, timedelta

from my_codegen.utils.report_utils import Reporter
from my_codegen.utils.logger import logger


class AssertionError(Exception):
    """Custom assertion error with detailed information."""

    def __init__(self, message: str, actual: Any = None, expected: Any = None) -> None:
        super().__init__(message)
        self.actual = actual
        self.expected = expected


class Validator:
    """Advanced validation and assertion utility with fluent interface.

    Provides human-readable error messages and detailed value formatting
    for better debugging experience.

    Example:
        expect(response.status_code, "status code").to_equal(200)
        expect(user.name, "user name").to_not_be_empty()
    """

    MAX_STRING_LENGTH = 200
    MAX_COLLECTION_PREVIEW = 5
    MAX_DICT_KEYS_PREVIEW = 3

    def __init__(self, actual: Any, name: str) -> None:
        """Initialize validator with actual value and descriptive name.

        Args:
            actual: The value to validate
            name: Descriptive name for the value (used in error messages)
        """
        self.actual = actual
        self._name = name
        self._negated = False

    @property
    def to_not(self) -> "Validator":
        """Create negated validator for inverse assertions.

        Returns:
            New validator instance with negated logic
        """
        new_validator = Validator(self.actual, self._name)
        new_validator._negated = not self._negated
        return new_validator

    def _format_value(self, value: Any, max_length: int = MAX_STRING_LENGTH) -> str:
        """Format value for display in error messages.

        Args:
            value: Value to format
            max_length: Maximum length for string representation

        Returns:
            Formatted string representation of the value
        """
        if value is None:
            return "None"

        if isinstance(value, str):
            if len(value) > max_length:
                return f"'{value[:max_length]}...' (truncated, full length: {len(value)})"
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
                return f"{result[:max_length]}... (truncated)"
            return result

    def _format_collection(self, value: Union[List, tuple], max_length: int) -> str:
        """Format list or tuple for display."""
        if len(value) == 0:
            return "[]" if isinstance(value, list) else "()"

        if value and hasattr(value[0], "__class__") and hasattr(value[0], "__dict__"):
            class_name = value[0].__class__.__name__
            return f"[{len(value)} objects of type {class_name}]"

        if len(value) <= self.MAX_COLLECTION_PREVIEW:
            formatted_items = [self._format_value(item, 50) for item in value]
            return f"[{', '.join(formatted_items)}]"
        else:
            preview_items = [self._format_value(item, 50) for item in value[:3]]
            return f"[{', '.join(preview_items)}, ... total {len(value)} items]"

    def _format_dict(self, value: Dict, max_length: int) -> str:
        """Format dictionary for display."""
        if not value:
            return "{}"

        if len(str(value)) <= max_length and len(value) <= 5:
            return str(value)

        keys = list(value.keys())[:self.MAX_DICT_KEYS_PREVIEW]
        key_preview = ", ".join(f"'{k}'" for k in keys)
        return f"{{dict with {len(value)} keys: {key_preview}, ...}}"

    def _format_set(self, value: Set, max_length: int) -> str:
        """Format set for display."""
        if not value:
            return "set()"

        if len(value) <= self.MAX_COLLECTION_PREVIEW:
            formatted_items = [self._format_value(item, 50) for item in list(value)]
            return f"{{{', '.join(formatted_items)}}}"
        else:
            preview_items = [self._format_value(item, 50) for item in list(value)[:3]]
            return f"{{{', '.join(preview_items)}, ... total {len(value)} items}}"

    def _format_object(self, value: Any) -> str:
        """Format custom object for display."""
        class_name = value.__class__.__name__
        if hasattr(value, "__dict__"):
            attrs = list(value.__dict__.keys())[:3]
            attr_preview = ", ".join(attrs)
            return f"{class_name}({attr_preview}, ...)"
        return f"{class_name} object"

    def _assert(self, condition: bool, error_msg: str, expected: Any = None) -> None:
        """Internal assertion method."""
        if self._negated:
            condition = not condition
            error_msg = error_msg.replace("Expected", "Expected NOT")

        if not condition:
            formatted_actual = self._format_value(self.actual)
            full_message = f"{error_msg}\\nActual {self._name}: {formatted_actual}"

            if expected is not None:
                formatted_expected = self._format_value(expected)
                full_message += f"\\nExpected: {formatted_expected}"

            logger.error(full_message)
            raise AssertionError(full_message, self.actual, expected)

    def to_equal(self, expected: Any) -> "Validator":
        """Assert that actual value equals expected value."""
        self._assert(
            self.actual == expected,
            f"Expected {self._name} to equal {self._format_value(expected)}",
            expected
        )
        return self

    def to_be_none(self) -> "Validator":
        """Assert that actual value is None."""
        self._assert(
            self.actual is None,
            f"Expected {self._name} to be None"
        )
        return self

    def to_be_empty(self) -> "Validator":
        """Assert that actual value is empty (for strings, lists, dicts, etc.)."""
        self._assert(
            len(self.actual) == 0,
            f"Expected {self._name} to be empty"
        )
        return self

    def to_contain(self, expected: Any) -> "Validator":
        """Assert that actual value contains expected item."""
        self._assert(
            expected in self.actual,
            f"Expected {self._name} to contain {self._format_value(expected)}",
            expected
        )
        return self

    def to_be_greater_than(self, expected: Union[int, float]) -> "Validator":
        """Assert that actual value is greater than expected."""
        self._assert(
            self.actual > expected,
            f"Expected {self._name} to be greater than {expected}",
            expected
        )
        return self

    def to_be_less_than(self, expected: Union[int, float]) -> "Validator":
        """Assert that actual value is less than expected."""
        self._assert(
            self.actual < expected,
            f"Expected {self._name} to be less than {expected}",
            expected
        )
        return self

    def to_match_pattern(self, pattern: str) -> "Validator":
        """Assert that actual string matches regex pattern."""
        self._assert(
            re.search(pattern, str(self.actual)) is not None,
            f"Expected {self._name} to match pattern '{pattern}'"
        )
        return self

    def to_be_instance_of(self, expected_type: type) -> "Validator":
        """Assert that actual value is instance of expected type."""
        self._assert(
            isinstance(self.actual, expected_type),
            f"Expected {self._name} to be instance of {expected_type.__name__}"
        )
        return self

    def to_have_length(self, expected_length: int) -> "Validator":
        """Assert that actual value has expected length."""
        actual_length = len(self.actual)
        self._assert(
            actual_length == expected_length,
            f"Expected {self._name} to have length {expected_length}, got {actual_length}",
            expected_length
        )
        return self


def expect(actual: Any, name: str = "value") -> Validator:
    """Create a new validator instance for fluent assertions.

    Args:
        actual: Value to validate
        name: Descriptive name for the value

    Returns:
        Validator instance for chaining assertions

    Example:
        expect(response.status_code, "status code").to_equal(200)
        expect(items, "item list").to_not.to_be_empty()
    """
    return Validator(actual, name)


# Backward compatibility aliases
Expect = Validator