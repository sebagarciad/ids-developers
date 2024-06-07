from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)
engine = create_engine("mysql+mysqlconnector://usuario:developers@localhost/tpintro_dev")


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
        return jsonify({'message': f'An error occurred: {str(err.__cause__)}'}), 500

@app.route('/sumar-aeropuerto', methods=['POST'])
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


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)