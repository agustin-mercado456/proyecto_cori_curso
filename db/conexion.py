import mysql.connector
from mysql.connector import Error

class ConexionDB:
    def __init__(self):
        # CAMBIA ESTOS DATOS POR LOS TUYOS
        self.config = {
            'host': 'localhost',
            'user': 'cori', 
            'password': '123', 
            'database': 'presupuesto'
        }
        self.connection = None

    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(**self.config)
            except Error as e:
                print(f"Error conectando a MySQL: {e}")
                return None
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()