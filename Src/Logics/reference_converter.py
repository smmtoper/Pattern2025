from typing import Any, Dict
from Src.Core.abstract_converter import AbstractConverter


class ReferenceConverter(AbstractConverter):
    """Конвертер для ссылочных (пользовательских) объектов."""

    def convert(self, obj: Any) -> Dict[str, Any]:
        if hasattr(obj, "__dict__"):
            return {k: v for k, v in obj.__dict__.items()}
        raise TypeError(f"ReferenceConverter поддерживает только объекты с __dict__, получено {type(obj)}")
