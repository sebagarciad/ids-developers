from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/informacion-usuario")
def info_usuario():
    return render_template('informacion-usuario.html')


'''@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404'''



if __name__ == "__main__":
    app.run("127.0.0.1", port="5000", debug=True)