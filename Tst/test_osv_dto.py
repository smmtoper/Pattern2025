import pytest
import json
from main import app

@pytest.fixture
def client():
    app.testing = True
    return app.app.test_client()

def test_osv_dto_structure(client):
    """Проверка, что API возвращает DTO-структуру, а не текст"""
    response = client.get(
        "/api/report/osv?start_date=2025-11-01&end_date=2025-11-03&warehouse=W001"
    )
    assert response.status_code == 200

    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

    first = data[0]
    # Проверяем структуру DTO
    assert "nomenclature" in first
    assert "warehouse" in first
    assert "unit" in first
    assert "opening_balance" in first
    assert "incoming" in first
    assert "outgoing" in first
    assert "closing_balance" in first

    # Проверяем, что номенклатура и склад — это объекты (DTO)
    assert isinstance(first["nomenclature"], dict)
    assert isinstance(first["warehouse"], dict)

    assert "name" in first["nomenclature"]
    assert "name" in first["warehouse"]


def test_osv_new_nomenclature_appears(client):
    """Проверка, что новая номенклатура появляется в ОСВ"""
    response = client.get(
        "/api/report/osv?start_date=2025-11-01&end_date=2025-11-03&warehouse=W002"
    )
    data = json.loads(response.data)

    nomenclatures = [d["nomenclature"]["name"] for d in data]
    assert "Деталь B" in nomenclatures
