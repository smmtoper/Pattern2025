from abc import ABC, abstractmethod
from typing import Any, Dict


class AbstractConverter(ABC):
    """Абстрактный базовый класс для всех конвертеров."""

    @abstractmethod
    def convert(self, obj: Any) -> Dict[str, Any]:
        """
        Метод должен вернуть словарь:
        ключ — наименование поля, значение — данные поля.
        """
        pass
