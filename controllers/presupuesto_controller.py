from services.presupuesto_service import PresupuestoService

class PresupuestoController:
    def __init__(self):
        # Instanciamos el servicio que se encargará de la Base de Datos
        self.service = PresupuestoService()

    def guardar_presupuesto_completo(self, datos_ui):
        print(datos_ui)
        # 1. Validaciones Básicas de Negocio
        if not datos_ui.get("id_cliente"):
            return False, "Error: Debe seleccionar o buscar un cliente válido."
            
        if not datos_ui.get("servicio_nombre"):
            return False, "Error: Debe seleccionar un tipo de servicio."

        try:
            # 2. El controlador llama al servicio para que ejecute la transacción SQL
            return self.service.guardar_presupuesto(datos_ui)
            

        except Exception as e:
            # Capturamos cualquier error raro de Python para que no se caiga el programa
            return False, f"Error inesperado en el controlador: {str(e)}"