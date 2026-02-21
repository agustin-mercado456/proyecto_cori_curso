from db.conexion import ConexionDB
from models.cliente import Cliente

class ClienteRepository:
    def __init__(self):
        self.db = ConexionDB()

    def obtener_todos(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        # 1. Agregamos 'direccion' al SELECT para que el modelo no explote
        cursor.execute("SELECT id_cliente, razon_social, cuit_cuil, rubro, localidad, provincia, direccion FROM clientes")
        res = cursor.fetchall()
        cursor.close()
        return [Cliente(**c) for c in res]

    def guardar(self, cliente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # 2. Corregida la doble coma en VALUES y falta de espacio en direccion
        sql = """INSERT INTO clientes (razon_social, cuit_cuil, rubro, localidad, provincia, direccion) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        valores = (cliente.razon_social, cliente.cuit_cuil, cliente.rubro, 
                   cliente.localidad, cliente.provincia, cliente.direccion)
        cursor.execute(sql, valores)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id

    def actualizar(self, cliente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # 3. Agregamos dirección al UPDATE para que sea consistente
        sql = """UPDATE clientes SET razon_social=%s, cuit_cuil=%s, rubro=%s, localidad=%s, provincia=%s, direccion=%s 
                 WHERE id_cliente=%s"""
        valores = (cliente.razon_social, cliente.cuit_cuil, cliente.rubro, 
                   cliente.localidad, cliente.provincia, cliente.direccion, cliente.id_cliente)
        cursor.execute(sql, valores)
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount > 0

    def eliminar(self, id_cliente):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        return rowcount > 0

    def buscar_cliente_por_cuit(self, cuit):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id_cliente, razon_social, cuit_cuil, rubro, localidad, provincia, direccion FROM clientes WHERE cuit_cuil = %s"
        cursor.execute(sql, (cuit,))
        res = cursor.fetchone()
        cursor.close()
        
        # Si la base de datos encuentra algo, armamos el objeto Cliente. Si no, devolvemos None.
        if res:
            return Cliente(**res)
        
        return None