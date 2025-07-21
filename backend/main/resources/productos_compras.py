from flask_restful import Resource, reqparse
from flask import make_response, jsonify, request
from .. import db
from ..models import ProductoCompraModel


class ProductosCompras(Resource):
    @staticmethod
    def get():
        productos_compras = ProductoCompraModel.query.all()
        return make_response(jsonify([pc.to_json() for pc in productos_compras]), 200)

    @staticmethod
    def post():
        parser = reqparse.RequestParser()
        parser.add_argument(
            "producto_id", type=int, required=True, help="Producto ID is required"
        )
        parser.add_argument(
            "compra_id", type=int, required=True, help="Compra ID is required"
        )
        parser.add_argument(
            "cantidad", type=int, required=True, help="Cantidad is required"
        )
        args = parser.parse_args()

        new_producto_compra = ProductoCompraModel.from_json(args)
        db.session.add(new_producto_compra)
        db.session.commit()

        return make_response(jsonify(new_producto_compra.to_json()), 201)


class ProductoCompraDetail(Resource):
    @staticmethod
    def get(producto_compra_id):
        producto_compra = ProductoCompraModel.query.get_or_404(producto_compra_id)
        return make_response(jsonify(producto_compra.to_json()), 200)

    @staticmethod
    def delete(producto_compra_id):
        producto_compra = ProductoCompraModel.query.get_or_404(producto_compra_id)
        db.session.delete(producto_compra)
        db.session.commit()
        return make_response(jsonify({"message": "ProductoCompra deleted"}), 204)
