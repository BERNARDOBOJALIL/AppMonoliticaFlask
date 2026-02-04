import sqlite3

def get_db():
    conn = sqlite3.connect("productos.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
   
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
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
    
    
    try:
        conn.execute("ALTER TABLE productOs ADD COLUMN categoria TEXT NOT NULL DEFAULT 'Miscelaneo'")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    
    conn.execute('''
        INSERT OR IGNORE INTO users (username, password)
        VALUES ('admin', '1234')
    ''')
    
    
    
    conn.commit()
    conn.close()

