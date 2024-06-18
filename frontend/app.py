from flask import Flask, render_template, request, redirect, url_for, current_app, session, flash
from datetime import datetime
import re
import requests
import secrets
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuraciones del servidor de correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'fiubaairlines@gmail.com'
app.config['MAIL_PASSWORD'] = 'urgb cifh xmwj dbzl'
app.config['MAIL_DEFAULT_SENDER'] = ('FIUBA Airlines', 'fiubaairlines@gmail.com')

mail = Mail(app)

app.secret_key = secrets.token_hex(16)

@app.route("/", methods=["GET", "POST"])
def home():
    fecha_actual = datetime.now().date()
    if request.method == "POST":
        desde = request.form.get("desde")
        hasta = request.form.get("hasta")
        fecha = request.form.get("fecha")

        error_vacio = {}
        if desde is None:
            error_vacio["desde"] = "Debe elegir una opción"
        if hasta is None:
            error_vacio["hasta"] = "Debe elegir una opción"

        try:
            mes, dia, año = fecha.split("/")
            fecha_input = datetime(int(año), int(mes), int(dia)).date()
            if fecha_actual > fecha_input:
                error_vacio["fecha"] = "Debe elegir una opción valida"
            else:
                fecha = fecha_input.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            error_vacio["fecha"] = "Debe elegir una opción valida"

        if error_vacio:
            return render_template('index.html', error_vacio=error_vacio, desde=desde, hasta=hasta, fecha=fecha)
        
        return redirect(url_for("resultados_busqueda", desde=desde, hasta=hasta, fecha=fecha))
    return render_template('index.html')

@app.route("/resultados-de-busqueda")
def resultados_busqueda():
    desde = request.args.get('desde')
    hasta = request.args.get('hasta')
    fecha = request.args.get('fecha')

    if not desde or not hasta or not fecha:
        current_app.logger.error('Missing parameters: desde, hasta, or fecha')
        return render_template('no-resultados.html')

    try:
        response = requests.get('http://localhost:8080/vuelos')
        response.raise_for_status()
        vuelos_data = response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Error fetching vuelos: {e}')
        return str(e), 500
    
    try:
        response = requests.get('http://localhost:8080/aeropuertos')
        response.raise_for_status()
        aeropuertos_data = response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f'Error fetching vuelos: {e}')
        return str(e), 500

    try:
        vuelos_filtrados = [
            vuelo for vuelo in vuelos_data
            if vuelo['codigo_aeropuerto_origen'] == desde and
               vuelo['codigo_aeropuerto_destino'] == hasta and
               vuelo['fecha_salida'] == fecha
        ]

        aeropuerto_origen = [
            aeropuerto for aeropuerto in aeropuertos_data
            if aeropuerto['codigo_aeropuerto'] == desde
        ]

        aeropuerto_destino = [
            aeropuerto for aeropuerto in aeropuertos_data
            if aeropuerto['codigo_aeropuerto'] == hasta
        ]

        if not vuelos_filtrados:
            current_app.logger.info('No se encontraron vuelos que coincidan')
            return render_template('no-resultados.html')
        
        if not aeropuerto_origen:
            current_app.logger.info('No se encontro el aeropuerto de origen')
            return render_template('no-resultados.html')
        
        if not aeropuerto_destino:
            current_app.logger.info('No se encontro el aeropuerto de destino')
            return render_template('no-resultados.html')

        vuelo = vuelos_filtrados[0]
        ciudad_origen = aeropuerto_origen[0]['ciudad']
        ciudad_destino = aeropuerto_destino[0]['ciudad']
        origen = vuelo['codigo_aeropuerto_origen']
        destino = vuelo['codigo_aeropuerto_destino']
        nro_vuelo = vuelo['id_vuelo']
        fecha_salida = vuelo['fecha_salida']
        fecha_llegada = vuelo['fecha_llegada']
        hora_salida = vuelo['hora_salida']
        hora_llegada = vuelo['hora_llegada']
        duracion = vuelo['duracion']
        precio = vuelo['precio']
        pasajes_disponibles = vuelo['pasajes_disponibles']
        codigo_aeropuerto_origen = vuelo['codigo_aeropuerto_origen']
        codigo_aeropuerto_destino = vuelo['codigo_aeropuerto_destino']

        session['origen'] = origen
        session['destino'] = destino
        session['nro_vuelo'] = nro_vuelo
        session['fecha_salida'] = fecha_salida
        session['hora_salida'] = hora_salida
        session['fecha_llegada'] = fecha_llegada
        session['hora_llegada'] = hora_llegada
        session['duracion'] = duracion
        session['precio'] = precio
        session['pasajes_disponibles'] = pasajes_disponibles 
        session['codigo_aeropuerto_origen'] = codigo_aeropuerto_origen 
        session['codigo_aeropuerto_destino'] = codigo_aeropuerto_destino 
        session['ciudad_origen'] = ciudad_origen
        session['ciudad_destino'] = ciudad_destino

        if not pasajes_disponibles:
            current_app.logger.info('No hay pasajes disponibles')
            return render_template('no-resultados.html')

        return render_template(
        'resultados-de-busqueda.html', 
        origen=origen, destino=destino, nro_vuelo=session['nro_vuelo'], 
        fecha_salida=session['fecha_salida'], fecha_llegada=session['fecha_llegada'], 
        hora_salida=session['hora_salida'], hora_llegada=session['hora_llegada'], 
        duracion=session['duracion'], precio=session['precio'], fecha=fecha, ciudad_origen=session['ciudad_origen'], ciudad_destino=session['ciudad_destino']
    )

    except KeyError as e:
        current_app.logger.error(f'Key error: {e}')
        return str(e), 500
    except Exception as e:
        current_app.logger.error(f'Unexpected error: {e}')
        return str(e), 500

@app.route("/informacion-usuario", methods=["GET", "POST"])
def info_usuario():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        dni = request.form.get("dni")
        mail = request.form.get("mail")
        
        errores_validacion = {}
        if not nombre:
            errores_validacion["nombre"] = "El nombre es obligatorio"
        if not apellido:
            errores_validacion["apellido"] = "El apellido es obligatorio"
        if not dni or not 7 <= len(dni) <= 8:
            errores_validacion["dni"] = "Ingresar un DNI valido."
        if not mail or not re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+(\.\w+){1,2}$', mail):
            errores_validacion["mail"] = "Ingresar una direccion de correo electronico valida"

        if errores_validacion:
            return render_template('informacion-usuario.html', errores_validacion=errores_validacion, nombre=nombre, apellido=apellido, dni=dni, mail=mail)
        
        # Almacenar datos de usuario en una user session
        session['nombre'] = nombre
        session['apellido'] = apellido
        session['dni'] = dni
        session['mail'] = mail

        # Diccionario para enviar datos a la API
        datos_usuarios = {
            "dni": dni,
            "nombre": nombre,
            "apellido": apellido,
            "mail": mail
        }

        # Envio de datos a la API
        try:
            api_response = requests.post("http://localhost:8080/usuarios", json=datos_usuarios)
            api_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error al enviar datos de usuario al API: {e}')
            return str(e), 500

        if api_response.status_code == 201 or api_response.status_code == 200:
            return redirect(url_for("pago"))
        else:
            return render_template('informacion-usuario.html', errores_validacion=errores_validacion, nombre=nombre, apellido=apellido, dni=dni, mail=mail)
    
    return render_template('informacion-usuario.html')



@app.route('/pago', methods=["GET", "POST"])
def pago():
    if request.method == "POST":
        nombre_titular = request.form.get("titular-tarjeta")
        numero_tarjeta = request.form.get("numero-tarjeta")
        vencimiento = request.form.get("vencimiento")
        codigo_seguridad = request.form.get("codigo-seguridad")
        dni_titular_tarjeta = request.form.get("dni-titular-tarjeta")

        errores_validacion = {}
        if not nombre_titular:
            errores_validacion["nombre_titular"] = "El nombre del titular es obligatorio"
        if not numero_tarjeta or not len(numero_tarjeta) == 16:
            errores_validacion["numero_tarjeta"] = "El número de la tarjeta debe ser válido"
        if not vencimiento or not len(vencimiento) == 5:
            errores_validacion["vencimiento"] = "La fecha de vencimiento debe ser válida"
        if not codigo_seguridad or not len(codigo_seguridad) == 3:
            errores_validacion["codigo_seguridad"] = "El código de seguridad debe ser válido"
        if not dni_titular_tarjeta or not 7 <= len(dni_titular_tarjeta) <= 8:
            errores_validacion["dni_titular"] = "Ingresar un DNI valido."
        if errores_validacion:
            return render_template('pago.html', errores_validacion=errores_validacion, nombre_titular=nombre_titular, 
                                   numero_tarjeta=numero_tarjeta, vencimiento=vencimiento, codigo_seguridad=codigo_seguridad)
        
        nombre = session.get('nombre')
        apellido = session.get('apellido')
        dni = session.get('dni')
        nro_vuelo = session.get('nro_vuelo')
        fecha_salida = session.get('fecha_salida')
        hora_salida = session.get('hora_salida')
        fecha_llegada = session.get('fecha_llegada')
        hora_llegada = session.get('hora_llegada')
        duracion = session.get('duracion')
        precio = session.get('precio')
        pasajes_disponibles = session.get('pasajes_disponibles')
        codigo_aeropuerto_origen = session.get('codigo_aeropuerto_origen')
        codigo_aeropuerto_destino = session.get('codigo_aeropuerto_destino')
        ciudad_origen = session.get('ciudad_origen')
        ciudad_destino = session.get('ciudad_destino')

        datos_transaccion = {
            "id_vuelo": nro_vuelo,
            "dni": dni,
            "total_transaccion": precio
        }

        datos_modificacion_de_vuelos = {
            'pasajes_disponibles': str(int(pasajes_disponibles)-1),
            'codigo_aeropuerto_origen': codigo_aeropuerto_origen,
            'codigo_aeropuerto_destino': codigo_aeropuerto_destino,
            'hora_salida': hora_salida,
            'hora_llegada': hora_llegada,
            'duracion': duracion,
            'precio': precio,
            "id_vuelo": nro_vuelo
        }

        try:
            api_response = requests.post("http://localhost:8080/transacciones", json=datos_transaccion)
            api_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error al enviar datos de usuario al API: {e}')
            return str(e), 500
        
        #Modifica la tabla vuelos para restarle un pasaje
        try:
            api_response = requests.patch(f"http://localhost:8080/vuelos/{nro_vuelo}", json=datos_modificacion_de_vuelos)
            api_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error al modificar los vuelos: {e}')
            return str(e), 500

        return redirect(url_for('compra_confirmada', nombre=nombre, apellido=apellido, dni=dni, 
                                nro_vuelo=nro_vuelo, fecha_salida=fecha_salida, 
                                hora_salida=hora_salida, fecha_llegada=fecha_llegada, 
                                hora_llegada=hora_llegada, duracion=duracion, precio=precio, ciudad_origen=ciudad_origen, 
                                ciudad_destino=ciudad_destino))



    return render_template('pago.html')


@app.route("/compra-confirmada", methods=["GET"])
def compra_confirmada():
    nombre = session.get('nombre')
    apellido = session.get('apellido')
    dni = session.get('dni')
    nro_vuelo = session.get('nro_vuelo')
    fecha_salida = session.get('fecha_salida')
    hora_salida = session.get('hora_salida')
    fecha_llegada = session.get('fecha_llegada')
    hora_llegada = session.get('hora_llegada')
    duracion = session.get('duracion')
    precio = session.get('precio')
    origen = session.get('origen')
    destino = session.get('destino')
    ciudad_origen = session.get('ciudad_origen')
    ciudad_destino = session.get('ciudad_destino')

    correo = session.get('mail')
    
    # Asunto fijo
    subject = f"Reserva de viaje {origen} - {destino} ({fecha_salida})"
    
    # Renderizar la plantilla HTML
    body = render_template('mail.html', nombre=nombre, apellido=apellido, dni=dni, 
                                nro_vuelo=nro_vuelo, fecha_salida=fecha_salida, 
                                hora_salida=hora_salida, fecha_llegada=fecha_llegada, 
                                hora_llegada=hora_llegada, duracion=duracion, precio=precio, origen=origen, 
                                destino=destino, ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino)

    msg = Message(subject, recipients=[correo])
    msg.html = body
    
    try:
        mail.send(msg)
        flash('Correo enviado con éxito!', 'success')
    except Exception as e:
        flash(f'Error al enviar el correo: {str(e)}', 'error')

    return render_template('compra-confirmada.html', nombre=nombre, apellido=apellido, dni=dni, 
                                nro_vuelo=nro_vuelo, fecha_salida=fecha_salida, 
                                hora_salida=hora_salida, fecha_llegada=fecha_llegada, 
                                hora_llegada=hora_llegada, duracion=duracion, precio=precio, origen=origen, 
                                destino=destino, ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino)


@app.route('/buscar-reserva', methods = ["GET", "POST"])
def buscar_reserva():
    if request.method == "POST":
        dni = request.form.get("dni")
        nro_vuelo = request.form.get("nro_vuelo")

        error_vacio = {}
        if not dni or not 7 <= len(dni) <= 8:
            error_vacio["dni"] = "Ingresar un DNI valido."
        if not nro_vuelo:
            error_vacio["nro_vuelo"] = "Debe ingresar el número de vuelo"
        if error_vacio:
            return render_template('buscar-reserva.html', error_vacio=error_vacio, dni=dni, nro_vuelo=nro_vuelo)
        
        try:
            response = requests.get('http://localhost:8080/transacciones')
            response.raise_for_status()
            reserva_data = response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error sl budvst transacciones: {e}')
            return str(e), 500

        try:
            response2= requests.get('http://localhost:8080/vuelos')
            response2.raise_for_status()
            vuelos_data = response2.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error al buscar vuelos: {e}')
            return str(e), 500
        
        try:
            response3 = requests.get('http://localhost:8080/usuarios')
            response3.raise_for_status()
            usuarios_data = response3.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error al buscar usuarios: {e}')
            return str(e), 500
        
        try:
            response = requests.get('http://localhost:8080/aeropuertos')
            response.raise_for_status()
            aeropuertos_data = response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error al buscar aeropuertos: {e}')
            return str(e), 500

        try:
            reserva = [
                dato for dato in reserva_data
                if dato['dni'] == int(dni) and
                dato['id_vuelo'] == int(nro_vuelo)
            ]

            vuelo_filtrado = [
                vuelo for vuelo in vuelos_data
                if vuelo['id_vuelo'] == int(nro_vuelo)
            ]

            usuario_filtrado = [
                usuario for usuario in usuarios_data
                if usuario['dni'] == int(dni)
            ]

            
            if not reserva:
                current_app.logger.info('No se encontro la reserva')
                return render_template('no-reserva.html')
            
            if not vuelo_filtrado:
                current_app.logger.info('No se encontro el vuelo')
                return render_template('no-reserva.html')
            
            if not usuario_filtrado:
                current_app.logger.info('No se encontro el usuario')
                return render_template('no-reserva.html')
            

            aeropuerto_origen = [
                aeropuerto for aeropuerto in aeropuertos_data
                if aeropuerto['codigo_aeropuerto'] == vuelo_filtrado[0]['codigo_aeropuerto_origen']
            ]

            aeropuerto_destino = [
                aeropuerto for aeropuerto in aeropuertos_data
                if aeropuerto['codigo_aeropuerto'] == vuelo_filtrado[0]['codigo_aeropuerto_origen']
            ]
            
            dato = reserva[0]
            vuelo = vuelo_filtrado[0]
            usuario = usuario_filtrado[0]
            origen = vuelo['codigo_aeropuerto_origen']
            destino = vuelo['codigo_aeropuerto_destino']
            nro_vuelo = dato['id_vuelo']
            duracion = vuelo['duracion']
            fecha_salida = vuelo['fecha_salida']
            fecha_llegada = vuelo['fecha_llegada']
            hora_salida = vuelo['hora_salida']
            hora_llegada = vuelo['hora_llegada']
            precio = vuelo['precio']
            nombre = usuario['nombre']
            apellido = usuario['apellido']
            dni = dato['dni']
            mail = usuario['mail']
            num_transaccion = dato['num_transaccion']
            ciudad_origen = aeropuerto_origen[0]['ciudad']
            ciudad_destino = aeropuerto_destino[0]['ciudad']

            return redirect(url_for('mi_reserva', 
                                origen=origen, destino=destino, nro_vuelo=nro_vuelo, 
                                fecha_salida=fecha_salida, fecha_llegada=fecha_llegada, hora_salida=hora_salida, hora_llegada=hora_llegada, 
                                precio=precio, nombre=nombre, apellido=apellido, dni=dni, mail=mail, duracion=duracion, num_transaccion=num_transaccion, 
                                ciudad_origen=ciudad_origen, ciudad_destino=ciudad_destino))
        except Exception as e:
            current_app.logger.error(f'Unexpected error: {e}')
            return str(e), 500
    return render_template('buscar-reserva.html')

@app.route('/mi-reserva', methods=["GET", "POST"])
def mi_reserva():
    if request.method == "GET":
        # Obtener parámetros de la URL
        origen = request.args.get('origen')
        destino = request.args.get('destino')
        nro_vuelo = request.args.get('nro_vuelo')
        fecha_salida = request.args.get('fecha_salida')
        fecha_llegada = request.args.get('fecha_llegada')
        hora_salida = request.args.get('hora_salida')
        hora_llegada = request.args.get('hora_llegada')
        precio = request.args.get('precio')
        nombre = request.args.get('nombre')
        apellido = request.args.get('apellido')
        dni = request.args.get('dni')
        mail = request.args.get('mail')
        duracion = request.args.get('duracion')
        num_transaccion = request.args.get('num_transaccion')
        
        try:
            response = requests.get('http://localhost:8080/aeropuertos')
            response.raise_for_status()
            aeropuertos_data = response.json()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error fetching vuelos: {e}')
            return str(e), 500
        
        aeropuerto_origen = [
            aeropuerto for aeropuerto in aeropuertos_data
            if aeropuerto['codigo_aeropuerto'] == origen
        ]

        aeropuerto_destino = [
            aeropuerto for aeropuerto in aeropuertos_data
            if aeropuerto['codigo_aeropuerto'] == destino
        ]

        ciudad_origen = aeropuerto_origen[0]['ciudad']
        ciudad_destino = aeropuerto_destino[0]['ciudad']

        # Guardar num_transaccion en la sesión
        session['num_transaccion'] = num_transaccion

        return render_template('mi-reserva.html', origen=origen, destino=destino, nro_vuelo=nro_vuelo, 
                               fecha_salida=fecha_salida, fecha_llegada=fecha_llegada, hora_salida=hora_salida, 
                               hora_llegada=hora_llegada, precio=precio, nombre=nombre, apellido=apellido, 
                               dni=dni, mail=mail, duracion=duracion, num_transaccion=num_transaccion, ciudad_origen=ciudad_origen, 
                               ciudad_destino=ciudad_destino)
    
    if request.method == "POST":
        num_transaccion = session.get('num_transaccion')

        if num_transaccion is None:
            current_app.logger.error('num_transaccion is None')
            return 'Error: num_transaccion is None', 400

        try:
            response = requests.delete(f'http://localhost:8080/transacciones/{num_transaccion}')
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f'Error borrando la transaccion de la base de datos: {e}')
            return str(e), 500
        
        return render_template('reserva-anulada.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.secret_key = secrets.token_hex(16)
    app.run("127.0.0.1", port="5001", debug=True)