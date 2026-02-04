import sqlite3

class Database:
    """Clase para manejar la conexión y operaciones con la base de datos"""
    
    DB_NAME = "productos.db"
    
    @staticmethod
    def get_connection():
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(Database.DB_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def init_db():
        """Inicializa la base de datos con las tablas necesarias"""
        conn = Database.get_connection()
       
        # Crear tabla de usuarios
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Crear tabla de productos
        conn.execute("""
        CREATE TABLE IF NOT EXISTS productOs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL CHECK (precio >= 0),
            stock INTEGER NOT NULL CHECK (stock >= 0),
            activo INTEGER NOT NULL CHECK (activo IN (0,1)),
            categoria TEXT NOT NULL DEFAULT 'Miscelaneo'
        )
        """)
        
        # Agregar columna categoría si no existe (para bases de datos existentes)
        try:
            conn.execute("ALTER TABLE productOs ADD COLUMN categoria TEXT NOT NULL DEFAULT 'Miscelaneo'")
            conn.commit()
        except sqlite3.OperationalError:
            # La columna ya existe
            pass
        
        # Insertar usuario admin por defecto
        conn.execute('''
            INSERT OR IGNORE INTO users (username, password)
            VALUES ('admin', '1234')
        ''')
        
        conn.commit()
        conn.close()
