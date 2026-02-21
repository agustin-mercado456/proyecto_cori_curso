from db.conexion import ConexionDB

class ConfigRepository:
    def __init__(self):
        self.db = ConexionDB()

    def obtener_precio_traslado(self, distancia_km):
        """Busca en la tabla de rangos el precio correspondiente"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Buscamos el rango donde encaja la distancia
        sql = "SELECT precio FROM tarifas_traslado WHERE %s BETWEEN km_min AND km_max"
        cursor.execute(sql, (distancia_km,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return float(result[0])
        return 0.0 # O manejar un valor por defecto si excede el rango máximo