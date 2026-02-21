from db.conexion import ConexionDB
from models.tipo_servicio import TipoServicio

class ServicioRepository:
    def __init__(self):
        self.db = ConexionDB()

    def obtener_todos(self):
        """Trae todos, incluso los inactivos, para poder reactivarlos si hace falta."""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipos_servicio")
        res = cursor.fetchall()
        cursor.close()
        return [TipoServicio(**s) for s in res]

    def obtener_activos(self):
        """Trae solo los que están disponibles para presupuestar."""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tipos_servicio WHERE activo = True")
        res = cursor.fetchall()
        cursor.close()
        return [TipoServicio(**s) for s in res]

    def guardar(self, servicio):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO tipos_servicio (nombre, descripcion, tarifa_base) VALUES (%s, %s, %s)"
        cursor.execute(sql, (servicio.nombre, servicio.descripcion, servicio.tarifa_base))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def actualizar(self, servicio):
        """Permite modificar nombre, descripción o tarifa."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = """UPDATE tipos_servicio 
                 SET nombre=%s, descripcion=%s, tarifa_base=%s, activo=%s 
                 WHERE id_tipo_servicio=%s"""
        valores = (servicio.nombre, servicio.descripcion, servicio.tarifa_base, 
                   servicio.activo, servicio.id_tipo_servicio)
        cursor.execute(sql, valores)
        conn.commit()
        res = cursor.rowcount > 0
        cursor.close()
        return res

    def baja_logica(self, id_tipo_servicio):
        """No elimina, solo desactiva."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE tipos_servicio SET activo = False WHERE id_tipo_servicio = %s"
        cursor.execute(sql, (id_tipo_servicio,))
        conn.commit()
        res = cursor.rowcount > 0
        cursor.close()
        return res