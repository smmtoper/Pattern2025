import connexion
from flask import request, jsonify
from datetime import datetime

from Src.Logics.convert_factory import ConvertFactory

app = connexion.FlaskApp(__name__)

# --- Пример данных рецептов ---
class Receipt:
    def __init__(self, code, name, ingredients, created):
        self.code = code
        self.name = name
        self.ingredients = ingredients  # список строк
        self.created = created  # datetime


# Пример "базы данных" рецептов
RECEIPTS_DB = [
    Receipt("R001", "Pancakes", ["Flour", "Milk", "Eggs"], datetime(2025, 1, 10)),
    Receipt("R002", "Omelette", ["Eggs", "Salt", "Pepper"], datetime(2025, 2, 5)),
    Receipt("R003", "Salad", ["Lettuce", "Tomato", "Cucumber"], datetime(2025, 3, 20)),
]


# --- REST API методы ---

@app.route("/api/accessibility", methods=['GET'])
def accessibility():
    return "SUCCESS"


@app.route("/api/GetReceipts", methods=['GET'])
def get_receipts():
    """
    Возвращает список всех рецептов.
    """
    result = [ConvertFactory.convert(r) for r in RECEIPTS_DB]
    return jsonify(result)


@app.route("/api/GetReceipt/<code>", methods=['GET'])
def get_receipt(code):
    """
    Возвращает конкретный рецепт по коду.
    """
    receipt = next((r for r in RECEIPTS_DB if r.code == code), None)
    if not receipt:
        return jsonify({"error": f"Рецепт с кодом {code} не найден"}), 404

    result = ConvertFactory.convert(receipt)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
