from flask import Blueprint, jsonify

main_bp = Blueprint("main_bp", __name__)


# RF: O sistema deve permitir que um usuario se autentique para obter um token
@main_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"mensagem": "Realizar um login"})


# RF: O Sistema deve permitir listagem de produtos
@main_bp.route("/products")
def get_products():
    return jsonify({"mensagem": "Esta é a rota de listagem dos produtos"})


# RF: O sistema deve permitir criação de produtos
@main_bp.route("/products", methods=["POST"])
def create_products():
    return jsonify({"mensagem": "Esta é a rota de criação do produto"})


# RF: O Sistema deve permitir visualizar os detalhes de um unico produto
@main_bp.route("/product/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    return jsonify(
        {
            "mensagem": f"Esta é a rota de visualização de detalhes do id do produto {product_id}"
        }
    )


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
