import pytest
from datetime import datetime
from Src.Logics.basic_converter import BasicConverter
from Src.Logics.datetime_converter import DatetimeConverter
from Src.Logics.reference_converter import ReferenceConverter


# === ТЕСТЫ ДЛЯ BasicConverter ===

def test_basic_converter_with_int():
    conv = BasicConverter()
    result = conv.convert(123)
    assert result == {"value": 123}


def test_basic_converter_with_float():
    conv = BasicConverter()
    result = conv.convert(3.14)
    assert result == {"value": 3.14}


def test_basic_converter_with_str():
    conv = BasicConverter()
    result = conv.convert("Hello")
    assert result == {"value": "Hello"}


def test_basic_converter_with_invalid_type():
    conv = BasicConverter()
    with pytest.raises(TypeError):
        conv.convert([1, 2, 3])


# === ТЕСТЫ ДЛЯ DatetimeConverter ===

def test_datetime_converter_valid():
    conv = DatetimeConverter()
    dt = datetime(2025, 10, 27, 15, 30, 45)
    result = conv.convert(dt)

    assert result["year"] == 2025
    assert result["month"] == 10
    assert result["day"] == 27
    assert result["time"] == "15:30:45"
    assert "value" in result and isinstance(result["value"], str)


def test_datetime_converter_invalid():
    conv = DatetimeConverter()
    with pytest.raises(TypeError):
        conv.convert("2025-10-27")


# === ТЕСТЫ ДЛЯ ReferenceConverter ===

class DummyObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value


def test_reference_converter_valid():
    conv = ReferenceConverter()
    obj = DummyObject("alpha", 42)
    result = conv.convert(obj)

    assert result == {"name": "alpha", "value": 42}


def test_reference_converter_invalid():
    conv = ReferenceConverter()
    with pytest.raises(TypeError):
        conv.convert(123)
