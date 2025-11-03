from typing import Any, Dict
from Src.Core.abstract_converter import AbstractConverter


class BasicConverter(AbstractConverter):
    """Конвертер для простых типов: int, float, str."""

    def convert(self, obj: Any) -> Dict[str, Any]:
        if isinstance(obj, (int, float, str)):
            return {"value": obj}
        raise TypeError(f"BasicConverter поддерживает только int, float, str, получено {type(obj)}")
