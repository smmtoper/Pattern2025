import connexion
from flask import request, jsonify
from datetime import datetime
import json
import os

from Src.Logics.models import Warehouse, Transaction
from Src.Logics.dto import NomenclatureDTO, WarehouseDTO, OSVRowDTO


app = connexion.FlaskApp(__name__)
app.add_api = app  # чтобы использовать Flask API-методы напрямую


# ======= Настройки =======
SETTINGS_FILE = "settings.json"


def load_settings():
    """Загрузка настроек из файла"""
    if not os.path.exists(SETTINGS_FILE):
        settings = {"first_start": True}
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
        return settings

    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_settings(settings):
    """Сохранение настроек"""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)


# ======= Стартовые данные =======
WAREHOUSES = []
TRANSACTIONS = []


def start_service():
    """Создание стартовых данных при запуске"""
    global WAREHOUSES, TRANSACTIONS
    print("Инициализация стартовых данных...")

    WAREHOUSES = [
        Warehouse("W001", "Главный склад"),
        Warehouse("W002", "Склад запасных частей"),
    ]

    TRANSACTIONS = [
        Transaction(datetime(2025, 11, 1), "T001", "Деталь A", WAREHOUSES[0], 50, "шт"),
        Transaction(datetime(2025, 11, 2), "T002", "Деталь A", WAREHOUSES[0], -10, "шт"),
        Transaction(datetime(2025, 11, 2), "T003", "Деталь B", WAREHOUSES[1], 25, "шт"),
        Transaction(datetime(2025, 11, 3), "T004", "Деталь A", WAREHOUSES[0], 40, "шт"),
    ]


# ======= Проверка настроек при запуске =======
settings = load_settings()

# Собираем справочник номенклатур из settings.json (если есть)
NOMENCLATURES_BY_NAME = {}
NOMENCLATURES_BY_ID = {}
if settings.get("default_receipt"):
    for n in settings["default_receipt"].get("nomenclatures", []):
        dto = NomenclatureDTO(
            id=n.get("id"),
            name=n.get("name"),
            range_id=n.get("range_id"),
            category_id=n.get("category_id"),
        )
        NOMENCLATURES_BY_NAME[dto.name] = dto
        if dto.id:
            NOMENCLATURES_BY_ID[dto.id] = dto

if settings.get("first_start", True):
    start_service()
    settings["first_start"] = False
    save_settings(settings)
else:
    print("Первый запуск уже выполнен — загружаем данные для текущей сессии")
    start_service()  # гарантируем, что данные инициализированы


# ======= API =======
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"


@app.route("/api/report/osv", methods=['GET'])
def get_osv():
    """Отчет ОСВ с возвратом DTO"""
    start_date_str = request.args.get("start_date")
    end_date_str = request.args.get("end_date")
    warehouse_code = request.args.get("warehouse")

    if not all([start_date_str, end_date_str, warehouse_code]):
        return jsonify({"error": "Укажите параметры start_date, end_date, warehouse"}), 400

    try:
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
    except ValueError:
        return jsonify({"error": "Некорректный формат даты. Используйте YYYY-MM-DD"}), 400

    wh = next((w for w in WAREHOUSES if w.code == warehouse_code), None)
    if not wh:
        return jsonify({"error": "Склад не найден"}), 404

    warehouse_dto = WarehouseDTO(code=wh.code, name=wh.name)

    wh_transactions = [t for t in TRANSACTIONS if t.warehouse.code == warehouse_code]

    # Список всех номенклатур из справочника
    all_nomenclatures = dict(NOMENCLATURES_BY_NAME)

    # Добавляем те, что появились в транзакциях, но не были в справочнике
    for t in wh_transactions:
        if t.nomenclature not in all_nomenclatures:
            all_nomenclatures[t.nomenclature] = NomenclatureDTO(
                id=None, name=t.nomenclature
            )

    report = {}
    for name, n_dto in all_nomenclatures.items():
        report[name] = {
            "dto": n_dto,
            "opening_balance": 0,
            "incoming": 0,
            "outgoing": 0,
        }

    for t in wh_transactions:
        n = t.nomenclature
        if n not in report:
            continue
        if t.date < start_date:
            report[n]["opening_balance"] += t.quantity
        elif start_date <= t.date <= end_date:
            if t.quantity > 0:
                report[n]["incoming"] += t.quantity
            else:
                report[n]["outgoing"] += abs(t.quantity)

    # Формируем результат в DTO-формате
    osv_result = []
    for name, data in report.items():
        rep = data
        closing = rep["opening_balance"] + rep["incoming"] - rep["outgoing"]
        row_dto = OSVRowDTO(
            nomenclature=rep["dto"],
            warehouse=warehouse_dto,
            unit="шт",
            opening_balance=rep["opening_balance"],
            incoming=rep["incoming"],
            outgoing=rep["outgoing"],
            closing_balance=closing,
        )
        osv_result.append(row_dto.to_dict())

    return jsonify(osv_result)


@app.route("/api/report/save", methods=['POST'])
def save_data():
    """Сохраняет все данные (склады и транзакции) в JSON"""
    data = {
        "warehouses": [w.to_dict() for w in WAREHOUSES],
        "transactions": [t.to_dict() for t in TRANSACTIONS],
    }

    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "warehouse_data.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return jsonify({"status": "OK", "saved_to": file_path})


if __name__ == '__main__':
    print("API запущен по адресу: http://127.0.0.1:8080")
    app.run(host="0.0.0.0", port=8080)
