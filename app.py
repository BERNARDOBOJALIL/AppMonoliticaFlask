from flask import Flask, render_template, request, redirect, url_for, session
from db import get_db, init_db

app = Flask(__name__)
app.secret_key = "clave_secreta_ficticia"

init_db()

# Aquí protegemos las rutas, todas requieren autenticación :)
@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", user=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# CRUD de productos
@app.route("/productos")
def productos():
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = get_db()
    productos = conn.execute("SELECT * FROM productOs WHERE activo = 1 ORDER BY id ASC").fetchall()
    conn.close()
    return render_template("productos.html", productos=productos)

@app.route("/productos/nuevo", methods=["GET", "POST"])
def productos_nuevo():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio = request.form.get("precio", "")
        stock = request.form.get("stock", "")
        activo = 1 if request.form.get("activo") else 0
        
        # Validaciones
        errores = []
        if not nombre:
            errores.append("El nombre no puede estar vacío")
        
        try:
            precio_num = float(precio)
            if precio_num < 0:
                errores.append("El precio no puede ser negativo")
        except ValueError:
            errores.append("El precio debe ser un número válido")
            precio_num = None
        
        try:
            stock_num = int(stock)
            if stock_num < 0:
                errores.append("El stock no puede ser negativo")
        except ValueError:
            errores.append("El stock debe ser un número entero válido")
            stock_num = None
        
        if errores:
            return render_template("producto_form.html", errores=errores, 
                                 nombre=nombre, precio=precio, stock=stock, 
                                 titulo="Nuevo Producto", accion="nuevo")
        
        conn = get_db()
        conn.execute(
            "INSERT INTO productOs (nombre, precio, stock, activo) VALUES (?, ?, ?, ?)",
            (nombre, precio_num, stock_num, activo)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("productos"))
    
    return render_template("producto_form.html", titulo="Nuevo Producto", accion="nuevo")

@app.route("/productos/<int:id>/editar", methods=["GET", "POST"])
def productos_editar(id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = get_db()
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio = request.form.get("precio", "")
        stock = request.form.get("stock", "")
        activo = 1 if request.form.get("activo") else 0
        
        # Validaciones
        errores = []
        if not nombre:
            errores.append("El nombre no puede estar vacío")
        
        try:
            precio_num = float(precio)
            if precio_num < 0:
                errores.append("El precio no puede ser negativo")
        except ValueError:
            errores.append("El precio debe ser un número válido")
            precio_num = None
        
        try:
            stock_num = int(stock)
            if stock_num < 0:
                errores.append("El stock no puede ser negativo")
        except ValueError:
            errores.append("El stock debe ser un número entero válido")
            stock_num = None
        
        if errores:
            producto = {"id": id, "nombre": nombre, "precio": precio, "stock": stock}
            conn.close()
            return render_template("producto_form.html", errores=errores, 
                                 producto=producto, titulo="Editar Producto", accion="editar")
        
        conn.execute(
            "UPDATE productOs SET nombre=?, precio=?, stock=?, activo=? WHERE id=?",
            (nombre, precio_num, stock_num, activo, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("productos"))
    
    producto = conn.execute("SELECT * FROM productOs WHERE id=?", (id,)).fetchone()
    conn.close()
    
    if not producto:
        return redirect(url_for("productos"))
    
    return render_template("producto_form.html", producto=producto, 
                         titulo="Editar Producto", accion="editar")

@app.route("/productos/<int:id>/eliminar", methods=["POST"])
def productos_eliminar(id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = get_db()
    conn.execute("DELETE FROM productOs WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("productos"))

if __name__ == "__main__":
    app.run(debug=True)
