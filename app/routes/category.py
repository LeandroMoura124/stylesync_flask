from flask import Blueprint, jsonify, request, current_app
from pydantic import ValidationError

from app.models.category import Category

category_bp = Blueprint("category_bp", __name__, url_prefix="/categories")

# Nome da collection no MongoDB
CATEGORIES_COLLECTION = "categories"


@category_bp.route("/", methods=["GET"])
def get_categories():
    db = current_app.config["db"]
    cursor = db[CATEGORIES_COLLECTION].find({})
    categories = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        categories.append(doc)
    return jsonify(categories)


@category_bp.route("/", methods=["POST"])
def create_category():
    try:
        raw_data = request.get_json() or {}
        category_data = Category(**raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    db = current_app.config["db"]
    doc = category_data.model_dump()
    result = db[CATEGORIES_COLLECTION].insert_one(doc)
    return (
        jsonify(
            {
                "message": "Categoria criada.",
                "id": str(result.inserted_id),
                **category_data.model_dump(),
            }
        ),
        201,
    ) 