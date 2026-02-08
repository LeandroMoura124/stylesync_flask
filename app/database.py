from pymongo import MongoClient
from app.config import MONGODB_URI, MONGODB_DB_NAME

# Cliente e banco são inicializados em create_app()
_client = None
db = None


def init_mongodb(app):
    """Inicializa a conexão com o MongoDB e armazena o banco em app.config."""
    global _client, db
    _client = MongoClient(MONGODB_URI)
    db = _client[MONGODB_DB_NAME]
    app.config["db"] = db

    @app.teardown_appcontext
    def close_connection(exception=None):
        # Opcional: fechar ao encerrar o app (Atlas mantém conexões em pool)
        pass
