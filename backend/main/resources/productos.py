from flask_restful import Resource, reqparse, abort
from flask import make_response, jsonify, request
from .. import db
from ..models import ProductoModel


class Productos(Resource):

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

        # Check if a product with the same name already exists
        existing_producto = ProductoModel.query.filter_by(nombre=args["nombre"]).first()
        if existing_producto:
            return make_response(
                jsonify({"message": "Producto with this name already exists"}), 400
            )

        new_producto = ProductoModel.from_json(args)
        db.session.add(new_producto)
        db.session.commit()

        return make_response(jsonify(new_producto.to_json()), 201)

    @staticmethod
    def get():
        productos = ProductoModel.query.all()
        return make_response(
            jsonify({
                "productos": [producto.to_json() for producto in productos]
                    }
            ),
        )




class ProductoDetail(Resource):
    @staticmethod
    def get(producto_id):

        producto = ProductoModel.query.get(producto_id)
        if not producto:
            abort(404, message="Producto no encontrado")

        return make_response(jsonify(producto.to_json()), 200)

    @staticmethod
    def put(producto_id):
        parser = reqparse.RequestParser()
        parser.add_argument("nombre", type=str, required=False)
        parser.add_argument("descripcion", type=str, required=False)
        parser.add_argument("imagen", type=str, required=False)
        parser.add_argument("precio", type=float, required=False)
        parser.add_argument("stock", type=int, required=False)
        args = parser.parse_args()

        producto = ProductoModel.query.get(producto_id)

        if not producto:
            abort(404, message="Producto no encontrado")


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
    def patch(producto_id):
        parser = reqparse.RequestParser()
        parser.add_argument("stock", type=int, required=True, help="Stock is required")
        args = parser.parse_args()

        producto = ProductoModel.query.get(producto_id)

        if not producto:
            abort(404, message="Producto no encontrado")

        producto.stock = args["stock"]

        db.session.commit()
        return make_response(jsonify(producto.to_json()), 200)

    @staticmethod
    def delete(producto_id):
        producto = ProductoModel.query.get(producto_id)

        if not producto:
            abort(404, message="Producto no encontrado")

        db.session.delete(producto)
        db.session.commit()
        return make_response(jsonify({"message": "Producto eliminado correctamente."}), 200)

