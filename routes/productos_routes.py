from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.productos_service import ProductosService

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

@productos_bp.route("/")
def productos():
    """Lista todos los productos con filtros y paginación"""
    if "user" not in session:
        return redirect(url_for("auth.login"))
    
    # Parámetros de búsqueda, filtro y paginación
    buscar = request.args.get("buscar", "").strip()
    filtro_activo = request.args.get("filtro", "todos")
    pagina = request.args.get("pagina", 1, type=int)
    por_pagina = 10
    
    productos, total_productos, total_paginas = ProductosService.get_productos_filtrados(
        buscar=buscar,
        filtro_activo=filtro_activo,
        pagina=pagina,
        por_pagina=por_pagina
    )
    
    return render_template("productos.html", 
                         productos=productos,
                         buscar=buscar,
                         filtro_activo=filtro_activo,
                         pagina=pagina,
                         total_paginas=total_paginas,
                         total_productos=total_productos)

@productos_bp.route("/nuevo", methods=["GET", "POST"])
def productos_nuevo():
    """Crea un nuevo producto"""
    if "user" not in session:
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio = request.form.get("precio", "")
        stock = request.form.get("stock", "")
        activo = 1 if request.form.get("activo") else 0
        categoria = request.form.get("categoria", "Miscelaneo").strip()
        
        if not categoria:
            categoria = "Miscelaneo"
        
        # Validar datos
        es_valido, errores, precio_num, stock_num = ProductosService.validar_producto(nombre, precio, stock)
        
        if not es_valido:
            for error in errores:
                flash(error, "error")
            return render_template("producto_form.html", errores=errores, 
                                 nombre=nombre, precio=precio, stock=stock, 
                                 titulo="Nuevo Producto", accion="nuevo")
        
        # Crear producto
        ProductosService.crear_producto(nombre, precio_num, stock_num, activo, categoria)
        
        estado = "activo" if activo else "inactivo"
        flash(f"Producto '{nombre}' creado exitosamente (${precio_num:.2f} - Stock: {stock_num} - Estado: {estado} - Categoría: {categoria})", "success")
        return redirect(url_for("productos.productos"))
    
    return render_template("producto_form.html", titulo="Nuevo Producto", accion="nuevo")

@productos_bp.route("/<int:id>/editar", methods=["GET", "POST"])
def productos_editar(id):
    """Edita un producto existente"""
    if "user" not in session:
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        precio = request.form.get("precio", "")
        stock = request.form.get("stock", "")
        activo = 1 if request.form.get("activo") else 0
        categoria = request.form.get("categoria", "Miscelaneo").strip()
        
        if not categoria:
            categoria = "Miscelaneo"
        
        # Validar datos
        es_valido, errores, precio_num, stock_num = ProductosService.validar_producto(nombre, precio, stock)
        
        if not es_valido:
            for error in errores:
                flash(error, "error")
            producto = {"id": id, "nombre": nombre, "precio": precio, "stock": stock, "categoria": categoria}
            return render_template("producto_form.html", errores=errores, 
                                 producto=producto, titulo="Editar Producto", accion="editar")
        
        # Actualizar producto
        ProductosService.actualizar_producto(id, nombre, precio_num, stock_num, activo, categoria)
        
        estado = "activo" if activo else "inactivo"
        flash(f"Producto '{nombre}' actualizado correctamente. Nuevo estado: {estado}, Precio: ${precio_num:.2f}, Stock: {stock_num}, Categoría: {categoria}", "success")
        return redirect(url_for("productos.productos"))
    
    # GET: mostrar formulario de edición
    producto = ProductosService.get_producto_by_id(id)
    
    if not producto:
        flash("El producto solicitado no existe o ha sido eliminado.", "error")
        return redirect(url_for("productos.productos"))
    
    return render_template("producto_form.html", producto=producto, 
                         titulo="Editar Producto", accion="editar")

@productos_bp.route("/<int:id>/eliminar", methods=["POST"])
def productos_eliminar(id):
    """Elimina un producto"""
    if "user" not in session:
        return redirect(url_for("auth.login"))
    
    exito, nombre = ProductosService.eliminar_producto(id)
    
    if exito:
        flash(f"El producto '{nombre}' ha sido eliminado permanentemente del sistema.", "success")
    else:
        flash("No se pudo eliminar el producto. Es posible que ya no exista.", "error")
    
    return redirect(url_for("productos.productos"))
