# Tst/test_osv_module.py

import pytest
from main import WAREHOUSES, TRANSACTIONS, app
import json

@pytest.fixture
def client():
    app.app.testing = True  # важно для Connexion
    with app.app.test_client() as client:
        yield client

def test_osv_report_basic(client):
    """Проверка ОСВ на корректность данных"""
    url = "/api/report/osv?start_date=2025-11-01&end_date=2025-11-03&warehouse=W001"
    response = client.get(url)
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))

    # Проверяем, что все номенклатуры из справочника присутствуют
    nomenclatures = [d["nomenclature"] for d in data]
    for name in ["Пшеничная мука", "Сахар", "Сливочное масло", "Яйцо", "Ванилин", "Деталь A"]:
        assert name in nomenclatures

    # Проверяем корректность приходов и расходов для "Деталь A"
    det_a = next(d for d in data if d["nomenclature"] == "Деталь A")
    assert det_a["incoming"] == 90
    assert det_a["outgoing"] == 10
    assert det_a["closing_balance"] == 80

def test_osv_invalid_params(client):
    """Проверка ОСВ при отсутствии обязательных параметров"""
    response = client.get("/api/report/osv")
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert "error" in data

def test_osv_warehouse_not_found(client):
    """Проверка ОСВ при неверном коде склада"""
    url = "/api/report/osv?start_date=2025-11-01&end_date=2025-11-03&warehouse=WRONG"
    response = client.get(url)
    assert response.status_code == 404
    data = json.loads(response.get_data(as_text=True))
    assert "error" in data
