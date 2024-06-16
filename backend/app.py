from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
import requests


app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://usuario:developers@localhost/tpintro_dev")

#
#
#    TABLA AEROPUERTOS
#
#
@app.route('/aeropuertos', methods=['GET'])
def aeropuertos():
    try:
        conn = engine.connect()
        query = "SELECT * FROM aeropuertos;"
        result = conn.execute(text(query))
        data = [
            {
                'codigo_aeropuerto': row[0],
                'nombre_aeropuerto': row[1],
                'ciudad': row[2],
                'pais': row[3]
            } for row in result
        ]
        conn.close()
        return jsonify(data), 200
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': f'Ocurrio un error: {str(err.__cause__)}'}), 500
      
@app.route('/aeropuertos', methods=['POST'])
def sumar_aeropuerto():
    conn = engine.connect()
    new_aeropuerto = request.get_json()
    query = text("""
        INSERT INTO aeropuertos (codigo_aeropuerto, nombre_aeropuerto, ciudad, pais)
        VALUES (:codigo_aeropuerto, :nombre_aeropuerto, :ciudad, :pais)
    """)
    try:
        result = conn.execute(query, {
            'codigo_aeropuerto': new_aeropuerto['codigo_aeropuerto'],
            'nombre_aeropuerto': new_aeropuerto['nombre_aeropuerto'],
            'ciudad': new_aeropuerto['ciudad'],
            'pais': new_aeropuerto['pais']
        })
        conn.commit()
        conn.close()
        return jsonify({'message': 'Se ha agregado correctamente'}), 201
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': f'Se ha producido un error: {str(err.__cause__)}'}), 500

@app.route('/aeropuertos/<codigo_aeropuerto>', methods = ['PATCH'])
def modificar_aeropuerto(codigo_aeropuerto):
    conn = engine.connect()
    mod_user = request.get_json()
    query = f"""UPDATE aeropuertos 
            SET nombre_aeropuerto = '{mod_user['nombre_aeropuerto']}' , ciudad = '{mod_user['ciudad']}' , pais = '{mod_user['pais']}'
            WHERE codigo_aeropuerto = {codigo_aeropuerto};"""
    query_validation = f"SELECT * FROM aeropuertos WHERE codigo_aeropuerto = {codigo_aeropuerto};"
    try:
        validation_result = conn.execute(text(query_validation))
        if validation_result.rowcount!=0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': "El aeropuerto no existe"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)})
    return jsonify({'message': 'se ha modificado correctamente' + query}), 200

@app.route('/aeropuertos/<codigo_aeropuerto>', methods = ['DELETE'])
def delete_aeropuerto(codigo_aeropuerto):
    conn = engine.connect()
    query = f"DELETE FROM aeropuertos WHERE codigo_aeropuerto = {codigo_aeropuerto};"
    validation_query = f"SELECT * FROM aeropuertos WHERE codigo_aeropuerto = {codigo_aeropuerto};"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": "El aeropuerto no existe"}), 404
    except SQLAlchemyError as err:
        jsonify(str(err.__cause__))
    return jsonify({'message': 'Se ha eliminado correctamente'}), 202

#
#
#   TABLA USUARIOS
#
#
@app.route('/usuarios', methods=['GET'])
def usuarios():
    try:
        with engine.connect() as conn:
            query = "SELECT * FROM usuarios;"
            result = conn.execute(text(query))
            data = [
                {
                    'dni': row[0],
                    'nombre': row[1],
                    'apellido': row[2],
                    'mail': row[3]
                } for row in result
            ]
            return jsonify(data), 200
    except SQLAlchemyError as e:
        return jsonify({'message': f'Error en la base de datos: {str(e)}'}), 500

@app.route('/usuarios/<dni>', methods = ['GET'])
def get_usuario(dni):
    conn = engine.connect()
    query = f"SELECT * FROM usuarios where dni = {dni};"
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__))
    if result.rowcount !=0:
        data = {}
        row = result.first()
        data['dni'] = row[0]
        data['nombre'] = row[1]
        data['apellido'] = row[2]
        data['mail'] = row[3]
        return jsonify(data), 200
    return jsonify({"message": "El usuario no existe"}), 404

@app.route('/usuarios', methods = ['POST'])
def crear_usuario():
    conn = engine.connect()
    new_user = request.get_json()
    query = text("""
                INSERT INTO usuarios (nombre, apellido, dni, mail) 
                VALUES (:nombre, :apellido, :dni, :mail) 
                """)
    try:
        result = conn.execute(query, {
            'dni': new_user['dni'],
            'nombre': new_user['nombre'],
            'apellido': new_user['apellido'],
            'mail': new_user['mail']
        })
        conn.commit()
        conn.close()
        return jsonify({'message': 'Se ha agregado correctamente'}), 201
    except SQLAlchemyError as err:
        return jsonify({'message': 'Se ha producido un error' + str(err.__cause__)})
    
@app.route('/usuarios/<dni>', methods = ['PATCH'])
def actualizar_usuario(dni):
    conn = engine.connect()
    mod_user = request.get_json()
    query = f"""UPDATE usuarios 
            SET nombre = "{mod_user['nombre']}" , apellido = "{mod_user['apellido']}" , mail = "{mod_user['mail']}"
            WHERE dni = {dni};"""
    query_validation = f"SELECT * FROM usuarios WHERE dni = {dni};"
    try:
        validation_result = conn.execute(text(query_validation))
        if validation_result.rowcount!=0:
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': "El usuario no existe"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)})
    return jsonify({'message': 'El usuario se ha modificado correctamente' + query}), 200    

@app.route('/usuarios/<dni>', methods = ['DELETE'])
def delete_usuario(dni):
    conn = engine.connect()
    query = f"DELETE FROM usuarios WHERE dni = {dni};"
    validation_query = f"SELECT * FROM usuarios WHERE dni = {dni}"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": "El usuario no existe"}), 404
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__)), 500
    return jsonify({'message': 'Se ha eliminado correctamente'}), 202

#
#
#   TABLA VUELOS
#
#
@app.route('/vuelos', methods=['GET'])
def vuelos():
    conn = engine.connect()
    query = "SELECT * FROM vuelos"
    try:
        result = conn.execute(text(query))
        conn.commit()
        conn.close()
    except SQLAlchemyError as err:
        return jsonify(str(err.cause)), 500

    data = []
    for row in result:
        entity = {
            'id_vuelo': row.id_vuelo,
            'codigo_aeropuerto_origen': row.codigo_aeropuerto_origen,
            'codigo_aeropuerto_destino': row.codigo_aeropuerto_destino,
            'fecha_salida': row.fecha_salida.strftime('%Y-%m-%d'),
            'fecha_llegada': row.fecha_llegada.strftime('%Y-%m-%d'),
            'hora_salida': str(row.hora_salida),
            'hora_llegada': str(row.hora_llegada),
            'duracion': str(row.duracion),
            'precio': row.precio,
            'pasajes_disponibles': row.pasajes_disponibles
        }
        data.append(entity)

    return jsonify(data), 200

@app.route('/vuelos', methods = ['POST'])
def agregar_vuelo():
    conn = engine.connect()
    nuevo_vuelo = request.get_json()
    query = text("""
        INSERT INTO vuelos (codigo_aeropuerto_origen, codigo_aeropuerto_destino, hora_salida, hora_llegada, duracion, precio, pasajes_disponibles)
        VALUES (:codigo_aeropuerto_origen, :codigo_aeropuerto_destino, :hora_salida, :hora_llegada, :duracion, :precio, :pasajes_disponibles)

    """)
    try:
        result = conn.execute(query, {
            'codigo_aeropuerto_origen': nuevo_vuelo['codigo_aeropuerto_origen'],
            'codigo_aeropuerto_destino': nuevo_vuelo['codigo_aeropuerto_destino'],
            'hora_salida': nuevo_vuelo['hora_salida'],
            'hora_llegada': nuevo_vuelo['hora_llegada'],
            'duracion': nuevo_vuelo['duracion'],
            'precio': nuevo_vuelo['precio'],
            'pasajes_disponibles': nuevo_vuelo['pasajes_disponibles']
        })
        conn.commit()
        conn.close()
        return jsonify({'message': 'Se ha agregado correctamente'}), 201
    except IntegrityError as err:
        conn.rollback()
        conn.close()
        return jsonify({'message': f'Se ha producido un error de integridad: {str(err)}'}), 400
    except KeyError as err:
        conn.close()
        return jsonify({'message': f'Se ha producido un error: Faltan campos requeridos ({str(err)})'}), 400
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': f'Se ha producido un error: {str(err.cause)}'}), 500

@app.route('/vuelos/<id_vuelo>', methods = ['PATCH'])
def actualizar_vuelo(id_vuelo):
    conn = engine.connect()
    act_vuelo = request.get_json()
    
    query = text("""
        UPDATE vuelos SET 
        pasajes_disponibles = :pasajes_disponibles, 
        codigo_aeropuerto_origen = :codigo_aeropuerto_origen, 
        codigo_aeropuerto_destino = :codigo_aeropuerto_destino, 
        hora_salida = :hora_salida, 
        hora_llegada = :hora_llegada, 
        duracion = :duracion, 
        precio = :precio
        WHERE id_vuelo = :id_vuelo
    """)
    
    query_validation = text("SELECT * FROM vuelos WHERE id_vuelo = :id_vuelo")
    
    try:
        validation_result = conn.execute(query_validation, {'id_vuelo': id_vuelo})
        
        if validation_result.rowcount != 0:
            conn.execute(query, {
                'pasajes_disponibles': act_vuelo['pasajes_disponibles'],
                'codigo_aeropuerto_origen': act_vuelo['codigo_aeropuerto_origen'],
                'codigo_aeropuerto_destino': act_vuelo['codigo_aeropuerto_destino'],
                'hora_salida': act_vuelo['hora_salida'],
                'hora_llegada': act_vuelo['hora_llegada'],
                'duracion': act_vuelo['duracion'],
                'precio': act_vuelo['precio'],
                'id_vuelo': id_vuelo
            })
            conn.commit()
            message = 'se ha modificado correctamente'
        else:
            message = 'El vuelo no existe'
            return jsonify({'message': message}), 404
    except SQLAlchemyError as err:
        conn.rollback()
        return jsonify({'message': str(err)}), 500
    finally:
        conn.close()
    
    return jsonify({'message': message}), 200

@app.route('/vuelos/<id_vuelo>', methods = ['DELETE'])
def delete_vuelo(id_vuelo):
    conn = engine.connect()
    query = f"""DELETE FROM vuelos
            WHERE id_vuelo = {id_vuelo};
            """
    validation_query = f"SELECT * FROM vuelos WHERE id_vuelo = {id_vuelo}"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": f"El vuelo {id_vuelo} no existe"}), 404
    except SQLAlchemyError as err:
        jsonify(str(err.__cause__))
    return jsonify({'message': 'El vuelo se ha eliminado correctamente'}), 202

#
#
#   TABLA TRANSACCIONES
#
#
@app.route('/transacciones', methods = ['GET'])
def transacciones():
    try:
        conn = engine.connect()
        query = "SELECT * FROM transacciones;"
        result = conn.execute(text(query))
        data = [
            {
                'num_transaccion': row[0],
                'id_vuelo': row[1],
                'total_transaccion': row[2],
                'dni': row[3]
            } for row in result
        ]
        conn.close()
        return jsonify(data), 200
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': f'Ocurrio un error: {str(err.__cause__)}'}), 500

@app.route('/transacciones', methods = ['POST'])
def crear_transaccion():
    conn = engine.connect()
    new_transaccion = request.get_json()
    query = text("""
        INSERT INTO transacciones (id_vuelo, total_transaccion, dni)
        VALUES (:id_vuelo, :total_transaccion, :dni)
    """)
    try:
        result = conn.execute(query, {
            'id_vuelo': new_transaccion['id_vuelo'],
            'total_transaccion': new_transaccion['total_transaccion'],
            'dni': new_transaccion['dni']
        })
        conn.commit()
        conn.close()
        return jsonify({'message': 'Se ha agregado correctamente'}), 201
    except IntegrityError as err:
        conn.rollback()
        conn.close()
        return jsonify({'message': f'Se ha producido un error de integridad: {str(err)}'}), 400
    except KeyError as err:
        conn.close()
        return jsonify({'message': f'Se ha producido un error: Faltan campos requeridos ({str(err)})'}), 400
    except SQLAlchemyError as err:
        conn.close()
        return jsonify({'message': f'Se ha producido un error: {str(err.__cause__)}'}), 500

@app.route('/transacciones/<num_transaccion>', methods = ['PATCH'])
def modificar_transacciones(num_transaccion):
    conn = engine.connect()
    mod_transaccion = request.get_json()
    query = text("""
            UPDATE transacciones
            SET id_vuelo = :id_vuelo, total_transaccion = :total_transaccion, dni = :dni
            WHERE num_transaccion = :num_transaccion
            """)
    query_validation = f"SELECT * FROM transacciones WHERE num_transaccion = {num_transaccion};"
    try:
        val_result = conn.execute(text(query_validation))
        if val_result.rowcount!=0:
            result = conn.execute(query, {
            'id_vuelo': mod_transaccion['id_vuelo'],
            'total_transaccion': mod_transaccion['total_transaccion'],
            'dni': mod_transaccion['dni'],
            'num_transaccion': num_transaccion
        })
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({'message': "La transacción no existe"}), 404
    except SQLAlchemyError as err:
        return jsonify({'message': str(err.__cause__)})
    return jsonify({'message': 'La transacción se ha modificado correctamente'}), 200

@app.route('/transacciones/<num_transaccion>', methods = ['DELETE'])
def delete_transaccion(num_transaccion):
    conn = engine.connect()
    query = f"""DELETE FROM transacciones
            WHERE num_transaccion = {num_transaccion};
            """
    validation_query = f"SELECT * FROM transacciones WHERE num_transaccion = {num_transaccion}"
    try:
        val_result = conn.execute(text(validation_query))
        if val_result.rowcount != 0 :
            result = conn.execute(text(query))
            conn.commit()
            conn.close()
        else:
            conn.close()
            return jsonify({"message": "La transaccion no existe"}), 404
    except SQLAlchemyError as err:
        return jsonify(str(err.__cause__)), 500
    return jsonify({'message': 'Se ha eliminado correctamente'}), 202

if __name__ == "__main__":
    app.run("127.0.0.1", port=8080, debug=True)