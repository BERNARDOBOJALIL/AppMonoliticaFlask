from flask import Flask, render_template, redirect, url_for, session
from repositories.database import Database
from routes.auth_routes import auth_bp
from routes.productos_routes import productos_bp

app = Flask(__name__)
app.secret_key = "clave_secreta_ficticia"

# Inicializar la base de datos
Database.init_db()

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(productos_bp)

@app.route("/")
def index():
    """Página principal"""
    if "user" not in session:
        return redirect(url_for("auth.login"))
    return render_template("index.html", user=session["user"])

if __name__ == "__main__":
    app.run(debug=True)
