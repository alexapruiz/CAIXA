from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/password")
def password():
    return render_template("password.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/usuarios/<nome_usuario>")
def usuarios(nome_usuario):
    return render_template("usuarios.html",nome_usuario=nome_usuario)


if __name__ == "__main__":
    app.run()