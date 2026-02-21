from repositories.servicio_repository import ServicioRepository

class ServicioService:
    def __init__(self):
        self.repo = ServicioRepository()

    def obtener_servicios_activos(self):
        """Devuelve solo los servicios que se pueden vender hoy."""
        return self.repo.obtener_activos()

    def obtener_todos_los_servicios(self):
        """Para la vista administrativa, devuelve todo el catálogo."""
        return self.repo.obtener_todos()

    def registrar_nuevo_servicio(self, servicio):
        """Valida y guarda un nuevo tipo de servicio."""
        # Lógica: Nombre en mayúsculas y quitar espacios
        servicio.nombre = servicio.nombre.strip().upper()
        
        # Lógica: Asegurar que la tarifa no sea negativa
        if servicio.tarifa_base < 0:
            servicio.tarifa_base = 0.0
            
        return self.repo.guardar(servicio)

    def actualizar_servicio(self, servicio):
        """Actualiza los datos de un servicio existente."""
        servicio.nombre = servicio.nombre.strip().upper()
        return self.repo.actualizar(servicio)

    def dar_de_baja_servicio(self, id_id):
        """Realiza la baja lógica para no perder historial."""
        # Aquí podrías agregar una validación: 
        # "No permitir dar de baja si es un servicio obligatorio por ley"
        return self.repo.baja_logica(id_id)