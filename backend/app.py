from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root:developers@localhost/tpintro")


@app.route('/aeropuertos', methods = ['GET'])
def aeropuertos():
    conn = engine.connect()
    
    query = "SELECT * FROM aeropuertos;"
    try:
        #Se debe usar text para poder adecuarla al execute de mysql-connector
        result = conn.execute(text(query))
        #Se hace commit de la consulta (acá no estoy seguro si es necesario para un select, sí es necesario para un insert!)
        conn.close() #Cerramos la conexion con la base de datos
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    
    #Se preparan los datos para ser mostrador como json
    data = []
    for row in result:
        entity = {}
        entity['codigo_aeropuerto'] = row.codigo_aeropuerto
        entity['nombre_aeropuerto'] = row.nombre_aeropuerto
        entity['ciudad'] = row.ciudad
        entity['pais'] = row.pais
        data.append(entity)

    return jsonify(data), 200

@app.route('/vuelos', methods = ['GET'])
def vuelos():
    conn = engine.connect()
    query = "SELECT * FROM vuelos"
    try:
        result = conn.execute(text(query))
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))

    data = []
    for row in result:
        entity = {}
        entity['codigo_aeropuerto_origen'] = row.codigo_aeropuerto_origen
        entity['codigo_aeropuerto_destino'] = row.codigo_aeropuerto_destino
        entity['hora_salida'] = row.hora_salida
        entity['hora_llegada'] = row.hora_llegada
        entity['duracion'] = row.duracion
        entity['precio'] = row.precio
        entity['pasajes_disponibles'] = row.pasajes_disponibles
        data.append(entity)

    return jsonify(data), 200


@app.route('/crear_transaccion', methods = ['POST'])
def crear_transaccion():
    conn = engine.connect()
    nueva_transaccion = request.get_json()
    #Se crea la query en base a los datos pasados por el endpoint.
    #Los mismos deben viajar en el body en formato JSON
    query = f"""INSERT INTO transacciones (id_vuelo, total_transaccion) VALUES '{nueva_transaccion["id_vuelo"]}', '{nueva_transaccion["total_transaccion"]}';"""
    try:
        result = conn.execute(text(query))
        #Una vez ejecutada la consulta, se debe hacer commit de la misma para que
        #se aplique en la base de datos.
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
    
    return jsonify({'message': 'se ha agregado correctamente' + query}), 201


@app.route('/vuelos/<id_vuelo>', methods = ['PATCH'])
def actualizar_vuelo(id_vuelo):
    conn = engine.connect()
    mod_vuelo = request.get_json()
    #De la misma manera que con el metodo POST los datos a modificar deberán
    #Ser enviados por medio del body de la request
    query = f"""UPDATE users SET pasajes_disponibles = '{mod_vuelo['pasajes_disponibles']}'
                WHERE id_vuelo = {id_vuelo};
            """
    query_validation = f"SELECT * FROM vuelos WHERE id_vuelos = {id_vuelo};"
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount!=0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': "El vuelo no existe"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)})
    return jsonify({'message': 'se ha modificado correctamente' + query}), 200


if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)