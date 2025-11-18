from datetime import datetime
from typing import Optional


class Warehouse:
    """
    Модель склада
    """
    def __init__(self, code: str, name: str, address: Optional[str] = None):
        self.code = code
        self.name = name
        self.address = address

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "address": self.address
        }


class Transaction:
    """
    Модель транзакции
    """
    def __init__(self,
                 date: datetime,
                 unique_number: str,
                 nomenclature: str,
                 warehouse: Warehouse,
                 quantity: float,
                 unit: str):
        self.date = date
        self.unique_number = unique_number
        self.nomenclature = nomenclature
        self.warehouse = warehouse
        self.quantity = quantity
        self.unit = unit

    def to_dict(self):
        """
        Преобразование транзакции в словарь (например, для JSON)
        """
        return {
            "date": self.date.isoformat(),
            "unique_number": self.unique_number,
            "nomenclature": self.nomenclature,
            "warehouse": self.warehouse.to_dict() if self.warehouse else None,
            "quantity": self.quantity,
            "unit": self.unit
        }
