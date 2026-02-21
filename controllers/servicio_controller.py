from services.servicio_service import ServicioService

class ServicioController:
    def __init__(self):
        self.service = ServicioService()

    def listar_servicios(self, solo_activos=True):
        """Obtiene la lista para llenar las tablas o combos."""
        if solo_activos:
            servicios = self.service.obtener_servicios_activos()
            print(servicios)
            return servicios

        return self.service.obtener_todos_los_servicios()

    def guardar_servicio(self, servicio):
        """Maneja la acción de guardar desde la vista."""
        if not servicio.nombre or servicio.tarifa_base is None:
            return False, "El nombre y la tarifa son obligatorios."
        
        try:
            self.service.registrar_nuevo_servicio(servicio)
            return True, "Servicio creado exitosamente."
        except Exception as e:
            return False, f"Error al guardar: {str(e)}"

    def modificar_servicio(self, servicio):
        """Maneja la actualización desde la vista."""
        try:
            if self.service.actualizar_servicio(servicio):
                return True, "Servicio actualizado correctamente."
            return False, "No se pudo encontrar el servicio para actualizar."
        except Exception as e:
            return False, f"Error: {str(e)}"

    def eliminar_servicio(self, id_id):
        """Maneja la baja lógica."""
        try:
            if self.service.dar_de_baja_servicio(id_id):
                return True, "Servicio desactivado del catálogo."
            return False, "Error al intentar desactivar."
        except Exception as e:
            return False, f"Error técnico: {str(e)}"