import pytest
from main import WAREHOUSES, TRANSACTIONS, app
import json
import matplotlib.pyplot as plt

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

    # Проверяем наличие номенклатур
    nomenclatures = [d["nomenclature"] for d in data]
    for name in ["Пшеничная мука", "Сахар", "Сливочное масло", "Яйцо", "Ванилин", "Деталь A"]:
        assert name in nomenclatures

    # Проверяем транзакции "Деталь A"
    det_a = next(d for d in data if d["nomenclature"] == "Деталь A")
    assert det_a["incoming"] == 90
    assert det_a["outgoing"] == 10
    assert det_a["closing_balance"] == 80

def test_osv_invalid_params(client):
    """Проверка ОСВ при отсутствии параметров"""
    response = client.get("/api/report/osv")
    assert response.status_code == 400
    data = json.loads(response.get_data(as_text=True))
    assert "error" in data

def test_osv_plot(client):
    """Интеграционный тест с визуализацией отчета ОСВ"""
    url = "/api/report/osv?start_date=2025-11-01&end_date=2025-11-03&warehouse=W001"
    response = client.get(url)
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))

    labels = [d["nomenclature"] for d in data]
    incoming = [d["incoming"] for d in data]
    outgoing = [d["outgoing"] for d in data]
    closing = [d["closing_balance"] for d in data]

    x = range(len(labels))
    plt.figure(figsize=(10,5))
    plt.bar(x, incoming, label="Приход")
    plt.bar(x, outgoing, bottom=incoming, label="Расход")
    plt.plot(x, closing, marker="o", color="red", label="Остаток")
    plt.xticks(x, labels, rotation=45, ha="right")
    plt.ylabel("Количество")
    plt.title("Оборотно-сальдовая ведомость")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Tst/osv_report.png")
    plt.close()
