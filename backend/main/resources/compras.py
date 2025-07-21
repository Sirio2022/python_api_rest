from flask_restful import Resource, reqparse
from flask import make_response, jsonify, request
from .. import db
from ..models import CompraModel


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


class CompraDetail(Resource):
    @staticmethod
    def get(compra_id):
        compra = CompraModel.query.get_or_404(compra_id)
        return make_response(jsonify(compra.to_json()), 200)

    @staticmethod
    def delete(compra_id):
        compra = CompraModel.query.get_or_404(compra_id)
        db.session.delete(compra)
        db.session.commit()
        return make_response(jsonify({"message": "Compra deleted"}), 204)
