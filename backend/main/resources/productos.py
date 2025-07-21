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

    @staticmethod
    def put():
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, required=True, help="ID is required")
        parser.add_argument("nombre", type=str, required=False)
        parser.add_argument("descripcion", type=str, required=False)
        parser.add_argument("imagen", type=str, required=False)
        parser.add_argument("precio", type=float, required=False)
        parser.add_argument("stock", type=int, required=False)
        args = parser.parse_args()

        producto = ProductoModel.query.get_or_404(args["id"])
        if args["nombre"] is not None:
            producto.nombre = args["nombre"]
        if args["descripcion"] is not None:
            producto.descripcion = args["descripcion"]
        if args["imagen"] is not None:
            producto.imagen = args["imagen"]
        if args["precio"] is not None:
            producto.precio = args["precio"]
        if args["stock"] is not None:
            producto.stock = args["stock"]

        db.session.commit()
        return make_response(jsonify(producto.to_json()), 200)

    @staticmethod
    def patch():
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, required=True, help="ID is required")
        parser.add_argument("stock", type=int, required=True, help="Stock is required")
        args = parser.parse_args()

        producto = ProductoModel.query.get_or_404(args["id"])
        producto.stock = args["stock"]

        db.session.commit()
        return make_response(jsonify(producto.to_json()), 200)

    @staticmethod
    def delete():
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, required=True, help="ID is required")
        args = parser.parse_args()

        producto = ProductoModel.query.get_or_404(args["id"])
        db.session.delete(producto)
        db.session.commit()
        return make_response(jsonify({"message": "Producto deleted"}), 204)


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
