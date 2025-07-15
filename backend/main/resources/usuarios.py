from flask_restful import Resource, reqparse
from flask import make_response, jsonify, request
from .. import db
from ..models import UsuarioModel


class Usuarios(Resource):
    @staticmethod
    def get():
        usuarios = UsuarioModel.query.all()
        return make_response(jsonify([usuario.to_json() for usuario in usuarios]), 200)

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username", type=str, required=True, help="Username is required"
        )
        parser.add_argument(
            "user_surname", type=str, required=True, help="User surname is required"
        )
        parser.add_argument("email", type=str, required=True, help="Email is required")
        parser.add_argument("role", type=str, default="user")
        parser.add_argument("phone_number", type=str, required=False)
        args = parser.parse_args()

        new_usuario = UsuarioModel.from_json(args)
        db.session.add(new_usuario)
        db.session.commit()

        return make_response(jsonify(new_usuario.to_json()), 201)


class Usuario(Resource):
    pass
