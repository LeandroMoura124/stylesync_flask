from flask import Blueprint, jsonify, request
from app.models.user import LoginPayLoad
from pydantic import ValidationError
from app import db
from bson import ObjectId
from app.models.product import ProductDBModel
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
        return jsonify({"message": "Login bem-sucedido"})
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
def create_products():
    return jsonify({"mensagem": "Esta é a rota de criação do produto"})


# RF: O Sistema deve permitir visualizar os detalhes de um unico produto
@main_bp.route("/products/<string:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify(
            {"error": f"Erro ao transformar o {product_id} em ObjectID: {e}"}
        ), 400

    product = db.products.find_one({'_id': oid})

    if product:
        product_dict = ProductDBModel(**product).model_dump(by_alias=True, exclude_none=True)
        return jsonify(product_dict)
    return jsonify(
        {"Erro": f"Erro ao encontrar produto id {product_id}"}
    ), 404


# RF: O Sistema deve permitir a atualização de um unico produto e o produto existente
@main_bp.route("/product/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    return jsonify(
        {"mensagem": f"Esta é a rota de atualização do produto com o id {product_id}"}
    )


# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    return jsonify(
        {"mensagem": f"Esta é a rota de deleção do produto com o id {product_id}"}
    )


# RF: O sistema deve permitir a importação de vendas atráves de um arquivo (csv)
@main_bp.route("/sales/upload", methods=["POST"])
def upload_sales():
    return jsonify({"mensagem": "Esta é a rota de upload do arquivo de vendas"})


@main_bp.route("/")
def index():
    return jsonify({"mensagem": "Bem vindo ao StyleSync"})
