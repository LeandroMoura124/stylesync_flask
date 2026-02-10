from flask import Blueprint, jsonify, request, current_app
from app.models.user import LoginPayLoad
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.product import Product, ProductDBModel, UpdateProduct
from app.decorators import token_required
from datetime import datetime, timedelta, timezone
import jwt


main_bp = Blueprint("main_bp", __name__)


# RF: O sistema deve permitir que um usuario se autentique para obter um token
@main_bp.route("/login", methods=["POST"])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayLoad(**raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Erro durante a requisição de dados"}), 500

    if user_data.username == "admin" and user_data.password == "123":
        token = jwt.encode(
            {
                "user_id": user_data.username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"message": "Credenciais inválidas"})


# RF: O Sistema deve permitir listagem de produtos
@main_bp.route("/products")
def get_products():
    products_cursor = db.products.find({})
    products_list = [
        ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        for product in products_cursor
    ]
    return jsonify(products_list)


# RF: O sistema deve permitir criação de produtos
@main_bp.route("/products", methods=["POST"])
@token_required
def create_products(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()})

    result = db.products.insert_one(product.model_dump())

    return (
        jsonify(
            {"mensagem": "Produto criado com sucesso!", "id": str(result.inserted_id)}
        ),
        201,
    )


# RF: O Sistema deve permitir visualizar os detalhes de um unico produto
@main_bp.route("/products/<string:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return (
            jsonify({"error": f"Erro ao transformar o {product_id} em ObjectID: {e}"}),
            400,
        )

    product = db.products.find_one({"_id": oid})

    if product:
        product_dict = ProductDBModel(**product).model_dump(
            by_alias=True, exclude_none=True
        )
        return jsonify(product_dict)
    return jsonify({"Erro": f"Erro ao encontrar produto id {product_id}"}), 404


# RF: O Sistema deve permitir a atualização de um unico produto e o produto existente
@main_bp.route("/product/<string:product_id>", methods=["PUT"])
@token_required
def update_product(token, product_id):
    try:
        oid = ObjectId(product_id)
        update_data = UpdateProduct(**request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()})
    
    update_result = db.products.update_one(
        {
            "_id": oid
        },
        {
            "$set": update_data.model_dump(exclude_unset=True)
        }
    )
    if update_result.matched_count == 0:
        return jsonify({"error": "Produto não encontrado"}), 404
    
    update_product = db.products.find_one({"_id": oid})
    return jsonify(
        ProductDBModel(**update_product).model_dump(by_alias=True, exclude=None)
    )


# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route("/product/<string:product_id>", methods=["DELETE"])
@token_required
def delete_product(token, product_id):
    try:
        oid = ObjectId(product_id)
    except Exception:
        return jsonify({"error: id do produto inválido"}), 400
    
    delect_product = db.products.delete_one({"_id": oid})
    
    if delect_product.deleted_count == 0:
        return jsonify({"error": "Produto não foi encontrado"}), 404
        
    return " ", 204


# RF: O sistema deve permitir a importação de vendas atráves de um arquivo (csv)
@main_bp.route("/sales/upload", methods=["POST"])
def upload_sales():
    return jsonify({"mensagem": "Esta é a rota de upload do arquivo de vendas"})


@main_bp.route("/")
def index():
    return jsonify({"mensagem": "Bem vindo ao StyleSync"})
