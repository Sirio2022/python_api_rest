import os
from flask import Flask, Blueprint
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

# Inicializa SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    load_dotenv()

    db_name = os.getenv("DB_NAME", "basecomercio.db")
    db_path = os.getenv("DB_PATH", "./")
    db_full_path = os.path.abspath(os.path.join(db_path, db_name))
    if db_path not in (".", "./") and not os.path.exists(db_path):
        os.makedirs(db_path, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_full_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Importa y registra los recursos aquí, después de inicializar db
    from main.resources import (
        ClientesResource,
        ClienteResource,
        UsuariosResource,
        UsuarioResource,
        ProductosResource,
        ProductoDetailResource,
        ComprasResource,
        CompraDetailResource,
        ProductosComprasResource,
        ProductoCompraDetailResource,
    )

    clientes_bp = Blueprint("clientes", __name__)
    api_clientes = Api(clientes_bp)
    api_clientes.add_resource(ClientesResource, "/clientes")
    api_clientes.add_resource(ClienteResource, "/clientes/<cliente_id>")

    usuarios_bp = Blueprint("usuarios", __name__)
    api_usuarios = Api(usuarios_bp)
    api_usuarios.add_resource(UsuariosResource, "/usuarios")
    api_usuarios.add_resource(UsuarioResource, "/usuario/<usuario_id>")

    productos_bp = Blueprint("productos", __name__)
    api_productos = Api(productos_bp)
    api_productos.add_resource(ProductosResource, "/productos")
    api_productos.add_resource(ProductoDetailResource, "/producto/<producto_id>")

    compras_bp = Blueprint("compras", __name__)
    api_compras = Api(compras_bp)
    api_compras.add_resource(ComprasResource, "/compras")
    api_compras.add_resource(CompraDetailResource, "/compra/<compra_id>")

    productos_compras_bp = Blueprint("productos_compras", __name__)
    api_productos_compras = Api(productos_compras_bp)
    api_productos_compras.add_resource(ProductosComprasResource, "/productos_compras")
    api_productos_compras.add_resource(ProductoCompraDetailResource, "/producto_compra/<producto_compra_id>")

    app.register_blueprint(clientes_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(compras_bp)
    app.register_blueprint(productos_compras_bp)

    with app.app_context():
        db.create_all()

    return app
