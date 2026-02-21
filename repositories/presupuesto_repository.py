from db.conexion import ConexionDB

class PresupuestoRepository:
    def __init__(self):
        self.db = ConexionDB()

    def guardar_presupuesto_completo(self, datos:dict):
        """
        Ejecuta 3 INSERTs en cascada utilizando transacciones para asegurar la integridad.
        """
        print('datos desde el repository', datos)
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            # Iniciamos una transacción: Todo se guarda junto, o no se guarda nada.
            conn.start_transaction()

            # ==========================================================
            # PASO 1: Insertar en la tabla principal (presupuestos)
            # ==========================================================
            sql_presupuesto = "INSERT INTO presupuestos (id_cliente, total,observaciones) VALUES (%s, %s, %s)"
            cursor.execute(sql_presupuesto, (datos["id_cliente"], datos["total"],"sin observaciones"))
            
            # Capturamos el ID generado automáticamente por MySQL
            id_presupuesto_generado = cursor.lastrowid

            # ==========================================================
            # PASO 2: Insertar en la tabla intermedia (presupuesto_detalle)
            # ==========================================================
            sql_detalle = "INSERT INTO presupuesto_detalle (id_presupuesto, id_tipo_servicio, cantidad) VALUES (%s, %s, 1)"
            # Usamos el ID que acabamos de capturar en el paso anterior
            cursor.execute(sql_detalle, (id_presupuesto_generado, datos["id_tipo_servicio"]))
            
            # Capturamos el ID del detalle
            id_detalle_generado = cursor.lastrowid

            # ==========================================================
            # PASO 3: Insertar en la tabla específica según el servicio
            # ==========================================================
            servicio = datos["servicio_nombre"]

            if servicio in ["Medicion de Ruido", "Medicion de Iluminacion"]:
                sql_esp = """INSERT INTO detalle_mediciones 
                             (id_detalle, kilometros, precio_km, cantidad_puestos, precio_por_puesto, requiere_croquis, precio_croquis) 
                             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                val_esp = (id_detalle_generado, datos["kilometros"], datos["precio_km"], 
                           datos["cantidad_puestos"], datos["precio_puesto"], 
                           datos["requiere_croquis"], datos["precio_croquis"])
                cursor.execute(sql_esp, val_esp)

            elif servicio == "RGRL":
                sql_esp = """INSERT INTO detalle_rgrl 
                             (id_detalle, kilometros, precio_km, cantidad_horas, precio_por_hora) 
                             VALUES (%s, %s, %s, %s, %s)"""
                val_esp = (id_detalle_generado, datos["kilometros"], datos["precio_km"], 
                           datos["cantidad_horas"], datos["precio_hora"])
                cursor.execute(sql_esp, val_esp)

            elif servicio == "Capacitacion":
                sql_esp = """INSERT INTO detalle_capacitacion 
                             (id_detalle, kilometros, precio_km, valor_capacitacion) 
                             VALUES (%s, %s, %s, %s)"""
                val_esp = (id_detalle_generado, datos["kilometros"], datos["precio_km"], 
                           datos["precio_capacitacion"])
                cursor.execute(sql_esp, val_esp)

            # ==========================================================
            # PASO 4: Confirmar la transacción
            # ==========================================================
            conn.commit()
            return True, f"Presupuesto guardado con éxito (Nº {id_presupuesto_generado})"

        except Exception as e:
            # Si ocurre CUALQUIER error en los pasos 1, 2 o 3, hacemos ROLLBACK
            # Esto deshace todos los INSERTs de este bloque.
            conn.rollback()
            return False, f"Error en la base de datos: {e}"
            
        finally:
            cursor.close()