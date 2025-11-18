import pytest
from datetime import datetime
from Src.Logics.models import Warehouse, Transaction


def test_warehouse_to_dict():
    wh = Warehouse(code="W001", name="Главный склад", address="ул. Промышленная, 1")
    data = wh.to_dict()
    assert data["code"] == "W001"
    assert data["name"] == "Главный склад"
    assert "address" in data


def test_transaction_to_dict():
    wh = Warehouse(code="W001", name="Главный склад")
    tr = Transaction(
        date=datetime(2025, 11, 3),
        unique_number="TRX123",
        nomenclature="Деталь A",
        warehouse=wh,
        quantity=10.5,
        unit="шт"
    )
    data = tr.to_dict()
    assert data["unique_number"] == "TRX123"
    assert data["warehouse"]["name"] == "Главный склад"
    assert data["quantity"] == 10.5
