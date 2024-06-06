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
        return redirect(url_for("prueba", desde=desde, hasta=hasta, fecha=fecha, adultos=adultos))
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
        pasaporte = request.form.get("pasaporte")
        mail = request.form.get("mail")
        
        errores_validacion = {}
        if not nombre:
            errores_validacion["nombre"] = "El nombre es obligatorio"
        if not apellido:
            errores_validacion["apellido"] = "El apellido es obligatorio"
        if not pasaporte or len(pasaporte) != 9:
            errores_validacion["pasaporte"] = "El pasaporte debe tener el formato AAA123456"
        if not mail or not re.match(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$', mail):
            errores_validacion["mail"] = "Ingresar una direccion de correo electronico valida"

        if errores_validacion:
            return render_template('informacion-usuario.html', errores_validacion=errores_validacion, nombre=nombre, apellido=apellido, pasaporte=pasaporte, mail=mail)
        
        return redirect(url_for("prueba", nombre=nombre, apellido=apellido, pasaporte=pasaporte, mail=mail))
    
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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)