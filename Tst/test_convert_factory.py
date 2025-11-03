import pytest
from datetime import datetime
from Src.Logics.convert_factory import ConvertFactory




# === Тестовые классы для ReferenceConverter ===
class Dummy:
    def __init__(self, name, age, birthday):
        self.name = name
        self.age = age
        self.birthday = birthday


# === ТЕСТЫ ДЛЯ ConvertFactory ===

# Простые типы
def test_basic_int():
    result = ConvertFactory.convert(42)
    assert result == {"value": 42}


def test_basic_float():
    result = ConvertFactory.convert(3.14)
    assert result == {"value": 3.14}


def test_basic_str():
    result = ConvertFactory.convert("Hello")
    assert result == {"value": "Hello"}


# Datetime
def test_datetime():
    dt = datetime(2025, 10, 27, 15, 30, 45)
    result = ConvertFactory.convert(dt)

    assert result["year"] == 2025
    assert result["month"] == 10
    assert result["day"] == 27
    assert result["time"] == "15:30:45"
    assert "value" in result and isinstance(result["value"], str)


# Составной объект (Reference)
def test_reference_object():
    dt = datetime(1990, 1, 1)
    obj = Dummy("Alice", 30, dt)
    result = ConvertFactory.convert(obj)

    # Проверяем, что все поля конвертированы
    assert "name" in result
    assert "age" in result
    assert "birthday" in result

    assert result["name"] == {"value": "Alice"}
    assert result["age"] == {"value": 30}
    assert result["birthday"]["year"] == 1990
    assert result["birthday"]["month"] == 1
    assert result["birthday"]["day"] == 1


# Ошибочный тип
def test_unsupported_type():
    with pytest.raises(TypeError):
        ConvertFactory.convert([1, 2, 3])
