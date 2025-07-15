import os
from flask import Flask, Blueprint
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask blueprint and API
clientes_bp = Blueprint("clientes", __name__)
api_clientes = Api(clientes_bp)

# Register resources with the API
api_clientes.add_resource(resources.ClientesResource, "/clientes")
api_clientes.add_resource(resources.ClienteResource, "/clientes/<cliente_id>")

# Initialize the SQLAlchemy object
db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    load_dotenv()

    # Configure the app with environment variables for a database
    db_name = os.getenv("DB_NAME", "basecomercio.db")
    db_path = os.getenv("DB_PATH", "./")
    db_full_path = os.path.abspath(os.path.join(db_path, db_name))
    if db_path not in (".", "./") and not os.path.exists(db_path):
        os.makedirs(db_path, exist_ok=True)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_full_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database
    db.init_app(app)
    app.register_blueprint(clientes_bp)
    with app.app_context():
        db.create_all()  # Create the database tables

    return app
