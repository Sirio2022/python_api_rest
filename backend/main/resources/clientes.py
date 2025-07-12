from flask_restful import Resource
from flask import make_response, jsonify


clientes = [
    {
        "id": 1,
        "nombre": "Juan",
        "apellido": "Gomez",
    },
    {
        "id": 2,
        "nombre": "Maria",
        "apellido": "Lopez",
    },
    {
        "id": 3,
        "nombre": "Carlos",
        "apellido": "Perez",
    },
]


class Clientes(Resource):
    def get(self):
        return jsonify({"clientes": clientes})


class Cliente(Resource):
    def get(self, cliente_id):
        try:
            cliente_id = int(cliente_id)
        except ValueError:
            return make_response(
                jsonify({"error": "El ID debe ser un número entero"}), 400
            )
        # expresión generadora. No comprensión de listas
        # Es más eficiente en memoria y velocidad. No genera una lista completa.
        cliente = next((c for c in clientes if c["id"] == cliente_id), None)
        if cliente:
            return jsonify({"cliente": cliente})
        else:
            return make_response(jsonify({"error": "Cliente not found"}), 404)
