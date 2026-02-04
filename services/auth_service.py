from repositories.database import Database

class AuthService:
    """Servicio para manejar la lógica de autenticación"""
    
    @staticmethod
    def authenticate_user(username, password):
        """
        Autentica un usuario con sus credenciales
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            
        Returns:
            dict: Usuario si las credenciales son correctas, None si no
        """
        conn = Database.get_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    @staticmethod
    def get_user_by_username(username):
        """
        Obtiene un usuario por su nombre de usuario
        
        Args:
            username: Nombre de usuario
            
        Returns:
            dict: Usuario si existe, None si no
        """
        conn = Database.get_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        ).fetchone()
        conn.close()
        
        return dict(user) if user else None
