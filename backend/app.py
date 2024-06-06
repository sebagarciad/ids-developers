from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://root@localhost/tpintro")


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




if __name__ == "__main__":
    app.run("127.0.0.1", port="5001", debug=True)