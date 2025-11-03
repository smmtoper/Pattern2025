from typing import Any, Dict
from datetime import datetime

from Src.Core.abstract_converter import AbstractConverter
from Src.Logics.basic_converter import BasicConverter
from Src.Logics.datetime_converter import DatetimeConverter
from Src.Logics.reference_converter import ReferenceConverter


class ConvertFactory:
    """
    Фабрика конвертеров.
    Принимает любой объект и формирует словарь(и) согласно структуре объекта.
    """

    @staticmethod
    def convert(obj: Any) -> Dict[str, Any]:
        """
        Выбирает подходящий конвертер по типу объекта и возвращает словарь.
        """

        # Простые типы
        if isinstance(obj, (int, float, str)):
            converter: AbstractConverter = BasicConverter()
            return converter.convert(obj)

        # Datetime
        if isinstance(obj, datetime):
            converter: AbstractConverter = DatetimeConverter()
            return converter.convert(obj)

        # Ссылочные объекты (с __dict__)
        if hasattr(obj, "__dict__"):
            converter: AbstractConverter = ReferenceConverter()
            result = {}
            # Рекурсивно конвертируем все поля объекта
            for key, value in obj.__dict__.items():
                result[key] = ConvertFactory.convert(value)
            return result

        # Если тип не поддерживается
        raise TypeError(f"ConvertFactory не поддерживает тип {type(obj)}")
