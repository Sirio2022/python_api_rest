from flask_restful import Resource
from flask import make_response, jsonify, request


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

    @staticmethod
    def get():
        return jsonify({"clientes": clientes})

    @staticmethod
    def post():
        nuevo_cliente = request.get_json()
        if not nuevo_cliente or not isinstance(nuevo_cliente, dict):
            return make_response(jsonify({"error": "Invalid input"}), 400)

        if "nombre" not in nuevo_cliente or "apellido" not in nuevo_cliente:
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        nuevo_cliente["id"] = len(clientes) + 1
        clientes.append(nuevo_cliente)
        return make_response(jsonify({"cliente": nuevo_cliente}), 201)


class Cliente(Resource):
    @staticmethod
    def get(cliente_id):
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

    @staticmethod
    def put(cliente_id):
        try:
            cliente_id = int(cliente_id)
        except ValueError:
            return make_response(
                jsonify({"error": "El ID debe ser un número entero"}), 400
            )
        datos = request.get_json()
        if not datos or not isinstance(datos, dict):
            return make_response(jsonify({"error": "Datos inválidos"}), 400)
        cliente = next((c for c in clientes if c["id"] == cliente_id), None)
        if cliente:
            cliente.update(
                {k: v for k, v in datos.items() if k in ["nombre", "apellido"]}
            )
            return jsonify({"cliente": cliente})
        else:
            return make_response(jsonify({"error": "Cliente no encontrado"}), 404)

    @staticmethod
    def delete(cliente_id):
        try:
            cliente_id = int(cliente_id)
        except ValueError:
            return make_response(
                jsonify({"error": "El ID debe ser un número entero"}), 400
            )
        global clientes
        cliente = next((c for c in clientes if c["id"] == cliente_id), None)
        if cliente:
            clientes = [c for c in clientes if c["id"] != cliente_id]
            return make_response(jsonify({"mensaje": "Cliente eliminado"}), 200)
        else:
            return make_response(jsonify({"error": "Cliente no encontrado"}), 404)
