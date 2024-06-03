from flask import Flask, render_template, request, redirect, url_for

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
        mail = request.form.get("correo")
        return redirect(url_for("prueba", nombre=nombre, apellido=apellido, pasaporte=pasaporte, mail=mail))
    return render_template('informacion-usuario.html')

@app.route("/resultados-de-busqueda")
def resultados_busqueda():
    return render_template('resultados-de-busqueda.html')


'''@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404'''



if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)