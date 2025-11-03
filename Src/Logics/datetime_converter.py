from datetime import datetime
from typing import Any, Dict
from Src.Core.abstract_converter import AbstractConverter


class DatetimeConverter(AbstractConverter):
    """Конвертер для объектов datetime."""

    def convert(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, datetime):
            return {
                "value": obj.isoformat(),
                "year": obj.year,
                "month": obj.month,
                "day": obj.day,
                "time": obj.strftime("%H:%M:%S")
            }
        raise TypeError(f"DatetimeConverter поддерживает только datetime, получено {type(obj)}")
