from flask_restful import Resource, reqparse
from flask import make_response, jsonify, request
from .. import db
from ..models import CompraModel


def _delete_compra_by_id(compra_id):
    compra = CompraModel.query.get_or_404(compra_id)
    db.session.delete(compra)
    db.session.commit()
    return make_response(jsonify({"message": "Compra deleted"}), 204)


class Compras(Resource):
    @staticmethod
    def get():
        compras = CompraModel.query.all()
        return make_response(jsonify([compra.to_json() for compra in compras]), 200)

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument(
            "usuario_id", type=int, required=True, help="Usuario ID is required"
        )
        args = parser.parse_args()

        new_compra = CompraModel.from_json(args)
        db.session.add(new_compra)
        db.session.commit()

        return make_response(jsonify(new_compra.to_json()), 201)

    @staticmethod
    def put():
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, required=True, help="ID is required")
        parser.add_argument("usuario_id", type=int, required=False)
        args = parser.parse_args()

        compra = CompraModel.query.get_or_404(args["id"])
        if args["usuario_id"] is not None:
            compra.usuario_id = args["usuario_id"]

        db.session.commit()
        return make_response(jsonify(compra.to_json()), 200)

    @staticmethod
    def delete():
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, required=True, help="ID is required")
        args = parser.parse_args()
        return _delete_compra_by_id(args["id"])


class CompraDetail(Resource):
    @staticmethod
    def get(compra_id):
        compra = CompraModel.query.get_or_404(compra_id)
        return make_response(jsonify(compra.to_json()), 200)

    @staticmethod
    def delete(compra_id):
        return _delete_compra_by_id(compra_id)
