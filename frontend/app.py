from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)



#Renderiza home
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        desde = request.form.get("desde")
        hasta = request.form.get("hasta")
        fecha = request.form.get("fecha")
        adultos = request.form.get("adultos")
        print(f"desde es = {desde}" )
        return redirect(url_for("resultados_busqueda", desde=desde, hasta=hasta, fecha=fecha, adultos=adultos))
    return render_template('index.html')

@app.route("/prueba")
def prueba():
    desde = request.args.get("desde", None)
    hasta = request.args.get("hasta", None)
    fecha = request.args.get("fecha", None)
    adultos = request.args.get("adultos", None)
    return render_template("prueba.html", desde=desde, hasta=hasta, fecha=fecha, adultos=adultos)

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
            errores_validacion["dni"] = "El pasaporte debe tener el formato AAA123456"
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
    datos_personales = {'nombre': 'juan', 'apellido': 'lopez'}
    datos_vuelo = {'destino': 'mendoza', 'fecha': '1/08/2024'}
    return render_template('compra-confirmada.html', datos_personales=datos_personales, datos_vuelo=datos_vuelo)

@app.route('/pago', methods=["GET", "POST"])
def pago():
    if request.method == "POST":
        nombre_titular = request.form.get("titular-tarjeta")
        numero_tarjeta = request.form.get("numero-tarjeta")
        vencimiento = request.form.get("vencimiento")
        codigo_seguridad = request.form.get("codigo-seguridad")

        errores_validacion = {}
        if not nombre_titular:
            errores_validacion["nombre_titular"] = "El nombre del titular es obligatorio"
        if not numero_tarjeta or not len(numero_tarjeta) == 16:
            errores_validacion["numero_tarjeta"] = "El número de la tarjeta debe ser válido"
        if not vencimiento or not len(vencimiento) == 5:
            errores_validacion["vencimiento"] = "La fecha de vencimiento debe ser válida"
        if not codigo_seguridad or not len(codigo_seguridad) == 3:
            errores_validacion["codigo_seguridad"] = "El código de seguridad debe ser válido"
        
        if errores_validacion:
            return render_template('pago.html', errores_validacion=errores_validacion, nombre_titular=nombre_titular, numero_tarjeta=numero_tarjeta, vencimiento=vencimiento, codigo_seguridad=codigo_seguridad)
        
        return redirect(url_for("compra_confirmada", nombre_titular=nombre_titular, numero_tarjeta=numero_tarjeta, vencimiento=vencimiento, codigo_seguridad=codigo_seguridad))


    return render_template('pago.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)