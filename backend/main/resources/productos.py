from flask_restful import Resource, reqparse
from flask import make_response, jsonify, request
from .. import db
from ..models import ProductoModel


class Productos(Resource):
    @staticmethod
    def get():
        productos = ProductoModel.query.all()
        return make_response(
            jsonify([producto.to_json() for producto in productos]), 200
        )

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument(
            "nombre", type=str, required=True, help="Nombre is required"
        )
        parser.add_argument("descripcion", type=str, required=False)
        parser.add_argument("imagen", type=str, required=False)
        parser.add_argument(
            "precio", type=float, required=True, help="Precio is required"
        )
        parser.add_argument("stock", type=int, default=0)
        args = parser.parse_args()

        new_producto = ProductoModel.from_json(args)
        db.session.add(new_producto)
        db.session.commit()

        return make_response(jsonify(new_producto.to_json()), 201)


class ProductoDetail(Resource):
    @staticmethod
    def get(producto_id):
        producto = ProductoModel.query.get_or_404(producto_id)
        return make_response(jsonify(producto.to_json()), 200)

    @staticmethod
    def delete(producto_id):
        producto = ProductoModel.query.get_or_404(producto_id)
        db.session.delete(producto)
        db.session.commit()
        return make_response(jsonify({"message": "Producto deleted"}), 204)
