from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import re

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    fecha_actual = datetime.now().date()
    if request.method == "POST":
        desde = request.form.get("desde")
        hasta = request.form.get("hasta")
        fecha = request.form.get("fecha")
        try:
            mes, dia, año = fecha.split("/")
        except ValueError:
            pass
        error_vacio = {}
        if desde == None:
            error_vacio["desde"] = "Debe elegir una opción"
        if hasta == None:
            error_vacio["hasta"] = "Debe elegir una opción"
        if not fecha or fecha_actual > datetime(int(año), int(mes), int(dia)).date():
            error_vacio["fecha"] = "Debe elegir una opción valida"
        
        if error_vacio:
            return render_template('index.html', error_vacio=error_vacio, desde=desde, hasta=hasta, fecha=fecha)
        return redirect(url_for("resultados_busqueda", desde=desde, hasta=hasta, fecha=fecha))
    return render_template('index.html')



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
        if not mail or not re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$', mail):
            errores_validacion["mail"] = "Ingresar una direccion de correo electronico valida"

        if errores_validacion:
            return render_template('informacion-usuario.html', errores_validacion=errores_validacion, nombre=nombre, apellido=apellido, dni=dni, mail=mail)
        
        return redirect(url_for("pago", nombre=nombre, apellido=apellido, dni=dni, mail=mail))
    
    return render_template('informacion-usuario.html')


@app.route("/resultados-de-busqueda")
def resultados_busqueda():
    origen = 'Buenos Aires'
    destino = 'Córdoba'
    nro_vuelo = 'AR1549'
    duracion = '1 hora 15 minutos'
    hora_salida = '15:00 hs'
    hora_llegada = '16:15 hs'
    precio = '$45000'
    fecha = '4/6/2024'
    informacion = [origen, destino, nro_vuelo, duracion, hora_salida, hora_llegada, precio, fecha]
    for elemento in informacion:
        if not elemento:
            return render_template('no-resultados.html')
    return render_template('resultados-de-busqueda.html', origen=origen, destino=destino, nro_vuelo=nro_vuelo, duracion=duracion, hora_salida=hora_salida, hora_llegada=hora_llegada, precio=precio, fecha=fecha)


@app.route("/compra-confirmada", methods=["GET"])
def compra_confirmada():
    origen = 'Buenos Aires'
    destino = 'Córdoba'
    nro_vuelo = 'AR1549'
    duracion = '1 hora 15 minutos'
    hora_salida = '15:00 hs'
    hora_llegada = '16:15 hs'
    precio = '$45000'
    fecha = '4/6/2024'
    nombre = 'Juan'
    apellido = 'Perez'
    dni = '12345678'
    mail = 'example@gmail.com'
    return render_template('compra-confirmada.html', origen=origen, destino=destino, nro_vuelo=nro_vuelo, duracion=duracion, hora_salida=hora_salida, hora_llegada=hora_llegada, precio=precio, fecha=fecha, nombre=nombre, apellido=apellido, dni=dni, mail=mail)


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
            return render_template('pago.html', errores_validacion=errores_validacion, nombre_titular=nombre_titular, numero_tarjeta=numero_tarjeta, vencimiento=vencimiento, codigo_seguridad=codigo_seguridad)
        
        return redirect(url_for("compra_confirmada", nombre_titular=nombre_titular, numero_tarjeta=numero_tarjeta, vencimiento=vencimiento, codigo_seguridad=codigo_seguridad, dni_titular_tarjeta=dni_titular_tarjeta))


    return render_template('pago.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)