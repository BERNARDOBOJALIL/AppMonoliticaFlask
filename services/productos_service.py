from repositories.database import Database

class ProductosService:
    """Servicio para manejar la lógica de negocio de productos"""
    
    @staticmethod
    def get_productos_filtrados(buscar="", filtro_activo="todos", pagina=1, por_pagina=10):
        """
        Obtiene productos con filtros y paginación
        
        Args:
            buscar: Texto para buscar en el nombre del producto
            filtro_activo: Filtro de estado ('todos', 'activos', 'inactivos')
            pagina: Número de página actual
            por_pagina: Cantidad de productos por página
            
        Returns:
            tuple: (productos, total_productos, total_paginas)
        """
        offset = (pagina - 1) * por_pagina
        conn = Database.get_connection()
        
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
        
        return productos, total_productos, total_paginas
    
    @staticmethod
    def crear_producto(nombre, precio, stock, activo, categoria="Miscelaneo"):
        """
        Crea un nuevo producto
        
        Args:
            nombre: Nombre del producto
            precio: Precio del producto
            stock: Cantidad en stock
            activo: Estado del producto (1=activo, 0=inactivo)
            categoria: Categoría del producto (por defecto 'Miscelaneo')
            
        Returns:
            int: ID del producto creado
        """
        if not categoria:
            categoria = "Miscelaneo"
            
        conn = Database.get_connection()
        cursor = conn.execute(
            "INSERT INTO productOs (nombre, precio, stock, activo, categoria) VALUES (?, ?, ?, ?, ?)",
            (nombre, precio, stock, activo, categoria)
        )
        conn.commit()
        producto_id = cursor.lastrowid
        conn.close()
        
        return producto_id
    
    @staticmethod
    def get_producto_by_id(producto_id):
        """
        Obtiene un producto por su ID
        
        Args:
            producto_id: ID del producto
            
        Returns:
            dict: Producto si existe, None si no
        """
        conn = Database.get_connection()
        producto = conn.execute("SELECT * FROM productOs WHERE id=?", (producto_id,)).fetchone()
        conn.close()
        
        return producto
    
    @staticmethod
    def actualizar_producto(producto_id, nombre, precio, stock, activo, categoria="Miscelaneo"):
        """
        Actualiza un producto existente
        
        Args:
            producto_id: ID del producto a actualizar
            nombre: Nuevo nombre del producto
            precio: Nuevo precio del producto
            stock: Nueva cantidad en stock
            activo: Nuevo estado del producto (1=activo, 0=inactivo)
            categoria: Nueva categoría del producto
            
        Returns:
            bool: True si se actualizó correctamente
        """
        if not categoria:
            categoria = "Miscelaneo"
            
        conn = Database.get_connection()
        conn.execute(
            "UPDATE productOs SET nombre=?, precio=?, stock=?, activo=?, categoria=? WHERE id=?",
            (nombre, precio, stock, activo, categoria, producto_id)
        )
        conn.commit()
        conn.close()
        
        return True
    
    @staticmethod
    def eliminar_producto(producto_id):
        """
        Elimina un producto por su ID
        
        Args:
            producto_id: ID del producto a eliminar
            
        Returns:
            tuple: (exito, nombre_producto)
        """
        conn = Database.get_connection()
        producto = conn.execute("SELECT nombre FROM productOs WHERE id=?", (producto_id,)).fetchone()
        
        if producto:
            conn.execute("DELETE FROM productOs WHERE id=?", (producto_id,))
            conn.commit()
            conn.close()
            return True, producto['nombre']
        
        conn.close()
        return False, None
    
    @staticmethod
    def validar_producto(nombre, precio, stock):
        """
        Valida los datos de un producto
        
        Args:
            nombre: Nombre del producto
            precio: Precio del producto
            stock: Stock del producto
            
        Returns:
            tuple: (es_valido, errores, precio_num, stock_num)
        """
        errores = []
        precio_num = None
        stock_num = None
        
        if not nombre or not nombre.strip():
            errores.append("El nombre no puede estar vacío")
        
        try:
            precio_num = float(precio)
            if precio_num < 0:
                errores.append("El precio no puede ser negativo")
        except (ValueError, TypeError):
            errores.append("El precio debe ser un número válido")
        
        try:
            stock_num = int(stock)
            if stock_num < 0:
                errores.append("El stock no puede ser negativo")
        except (ValueError, TypeError):
            errores.append("El stock debe ser un número entero válido")
        
        es_valido = len(errores) == 0
        return es_valido, errores, precio_num, stock_num
