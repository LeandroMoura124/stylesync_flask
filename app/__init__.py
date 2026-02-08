from flask import Flask
from pymongo import MongoClient


db = None

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    global db

    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client[app.config['MONGO_DB_NAME']]
        app.config['db'] = db
    except Exception as e:
        print(f"Erro ao realizar a conexao com o banco de dados: {e}")

    from .routes.category import category_bp
    from .routes.main import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(category_bp)

    return app
