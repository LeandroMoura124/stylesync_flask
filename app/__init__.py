from flask import Flask
from .routes.main import main_bp
from .routes.category import category_bp
from .database import init_mongodb


def create_app():
    app = Flask(__name__)
    init_mongodb(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(category_bp)
    return app