from flask import Flask, render_template, request, redirect, url_for, session, flash
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
            flash(f"Bienvenido de nuevo, {user['username']}. Has iniciado sesión correctamente.", "success")
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos. Por favor, verifica tus credenciales e intenta nuevamente.", "error")
            return render_template("login.html")

    return render_template("login.html")

@app.route("/logout")
def logout():
    usuario = session.get("user", "Usuario")
    session.clear()
    flash(f"Hasta pronto, {usuario}. Has cerrado sesión de forma segura.", "info")
    return redirect(url_for("login"))

# CRUD de productos
@app.route("/productos")
def productos():
    if "user" not in session:
        return redirect(url_for("login"))
    
    # Parámetros de búsqueda, filtro y paginación
    buscar = request.args.get("buscar", "").strip()
    filtro_activo = request.args.get("filtro", "todos")  # todos, activos, inactivos
    pagina = request.args.get("pagina", 1, type=int)
    por_pagina = 10
    offset = (pagina - 1) * por_pagina
    
    conn = get_db()
    
    # Construir consulta SQL con filtros
    sql = "SELECT * FROM productOs WHERE 1=1"
    params = []
    
    # Filtro de búsqueda por nombre
    if buscar:
        sql += " AND nombre LIKE ?"
        params.append(f"%{buscar}%")
    
    # Filtro de activo/inactivo
    if filtro_activo == "activos":
        sql += " AND activo = 1"
    elif filtro_activo == "inactivos":
        sql += " AND activo = 0"
    
    # Contar total de productos
    count_sql = sql.replace("SELECT *", "SELECT COUNT(*)")
    total_productos = conn.execute(count_sql, params).fetchone()[0]
    total_paginas = (total_productos + por_pagina - 1) // por_pagina
    
    # Agregar orden y paginación
    sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([por_pagina, offset])
    
    productos = conn.execute(sql, params).fetchall()
    conn.close()
    
    return render_template("productos.html", 
                         productos=productos,
                         buscar=buscar,
                         filtro_activo=filtro_activo,
                         pagina=pagina,
                         total_paginas=total_paginas,
                         total_productos=total_productos)

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
            for error in errores:
                flash(error, "error")
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
        estado = "activo" if activo else "inactivo"
        flash(f"Producto '{nombre}' creado exitosamente (${precio_num:.2f} - Stock: {stock_num} - Estado: {estado})", "success")
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
            for error in errores:
                flash(error, "error")
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
        estado = "activo" if activo else "inactivo"
        flash(f"Producto '{nombre}' actualizado correctamente. Nuevo estado: {estado}, Precio: ${precio_num:.2f}, Stock: {stock_num}", "success")
        return redirect(url_for("productos"))
    
    producto = conn.execute("SELECT * FROM productOs WHERE id=?", (id,)).fetchone()
    conn.close()
    
    if not producto:
        flash("El producto solicitado no existe o ha sido eliminado.", "error")
        return redirect(url_for("productos"))
    
    return render_template("producto_form.html", producto=producto, 
                         titulo="Editar Producto", accion="editar")

@app.route("/productos/<int:id>/eliminar", methods=["POST"])
def productos_eliminar(id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = get_db()
    producto = conn.execute("SELECT nombre FROM productOs WHERE id=?", (id,)).fetchone()
    if producto:
        conn.execute("DELETE FROM productOs WHERE id=?", (id,))
        conn.commit()
        flash(f"El producto '{producto['nombre']}' ha sido eliminado permanentemente del sistema.", "success")
    else:
        flash("No se pudo eliminar el producto. Es posible que ya no exista.", "error")
    conn.close()
    return redirect(url_for("productos"))

if __name__ == "__main__":
    app.run(debug=True)
