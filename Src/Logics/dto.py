from typing import Optional, Dict, Any

class WarehouseDTO:
    def __init__(self, code: str, name: str, address: Optional[str] = None):
        self.code = code
        self.name = name
        self.address = address

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "name": self.name,
            "address": self.address
        }


class NomenclatureDTO:
    def __init__(self, id: Optional[str], name: str, range_id: Optional[str] = None, category_id: Optional[str] = None):
        self.id = id
        self.name = name
        self.range_id = range_id
        self.category_id = category_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "range_id": self.range_id,
            "category_id": self.category_id
        }


class OSVRowDTO:
    """
    DTO для одной строки ОСВ
    полями:
      - opening_balance, nomenclature (объект), unit, incoming, outgoing, closing_balance, warehouse (объект)
    """
    def __init__(self,
                 nomenclature: NomenclatureDTO,
                 unit: str,
                 opening_balance: float = 0,
                 incoming: float = 0,
                 outgoing: float = 0,
                 closing_balance: float = 0,
                 warehouse: Optional[WarehouseDTO] = None):
        self.nomenclature = nomenclature
        self.unit = unit
        self.opening_balance = opening_balance
        self.incoming = incoming
        self.outgoing = outgoing
        self.closing_balance = closing_balance
        self.warehouse = warehouse

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nomenclature": self.nomenclature.to_dict(),
            "unit": self.unit,
            "opening_balance": self.opening_balance,
            "incoming": self.incoming,
            "outgoing": self.outgoing,
            "closing_balance": self.closing_balance,
            "warehouse": self.warehouse.to_dict() if self.warehouse else None
        }
