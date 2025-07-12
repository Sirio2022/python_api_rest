import os
from flask import Flask, Blueprint
from dotenv import load_dotenv
from flask_restful import Api
import main.resources as resources

# Initialize the Flask blueprint and API
clientes_bp = Blueprint("clientes", __name__)
api_clientes = Api(clientes_bp)

# Register resources with the API
api_clientes.add_resource(resources.ClientesResource, "/clientes")
api_clientes.add_resource(resources.ClienteResource, "/clientes/<cliente_id>")


def create_app():

    app = Flask(__name__)

    load_dotenv()

    app.register_blueprint(clientes_bp)

    return app
