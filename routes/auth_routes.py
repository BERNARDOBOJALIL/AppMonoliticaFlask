from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Ruta para el inicio de sesión"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = AuthService.authenticate_user(username, password)

        if user:
            session["user"] = user["username"]
            flash(f"Bienvenido de nuevo, {user['username']}. Has iniciado sesión correctamente.", "success")
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos. Por favor, verifica tus credenciales e intenta nuevamente.", "error")
            return render_template("login.html")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    """Ruta para cerrar sesión"""
    usuario = session.get("user", "Usuario")
    session.clear()
    flash(f"Hasta pronto, {usuario}. Has cerrado sesión de forma segura.", "info")
    return redirect(url_for("auth.login"))
