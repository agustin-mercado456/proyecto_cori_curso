from services.cliente_service import ClienteService

class ClienteController:
    def __init__(self):
        self.service = ClienteService()

    def listar_clientes(self):
        return self.service.obtener_lista_clientes()

    def guardar_cliente(self, cliente):
        if not cliente.razon_social or not cliente.cuit_cuil:
            return False, "Razón Social y CUIT son obligatorios."
        try:
            id_nuevo = self.service.registrar_cliente(cliente)
            return True, f"Cliente guardado con ID: {id_nuevo}"
        except Exception as e:
            return False, f"Error en servicio: {e}"

    def actualizar_cliente(self, cliente):
        try:
            if self.service.actualizar_datos_cliente(cliente):
                return True, "Cliente actualizado correctamente."
            return False, "No se pudo actualizar."
        except Exception as e:
            return False, f"Error: {e}"

    def eliminar_cliente(self, id_cliente):
        try:
            return self.service.dar_de_baja(id_cliente)
        except Exception as e:
            return False

    def buscar_cliente_por_cuit(self, cuit):
        return self.service.buscar_por_cuit(cuit)