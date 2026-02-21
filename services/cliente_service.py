from repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def obtener_lista_clientes(self):
        # Lógica: Traer todos y ordenarlos por Razón Social
        clientes = self.repository.obtener_todos()
        return sorted(clientes, key=lambda c: c.razon_social)

    def registrar_cliente(self, cliente):
        # Lógica de Negocio: Limpiar datos antes de guardar
        cliente.razon_social = cliente.razon_social.strip().upper()
        cliente.direccion = cliente.direccion.strip().upper()
        cliente.localidad = cliente.localidad.strip().upper()
        
        return self.repository.guardar(cliente)

    def actualizar_datos_cliente(self, cliente):
        cliente.razon_social = cliente.razon_social.strip().upper()
        return self.repository.actualizar(cliente)

    def dar_de_baja(self, id_cliente):
        return self.repository.eliminar(id_cliente)

    def buscar_por_cuit(self, cuit):
        return self.repository.buscar_cliente_por_cuit(cuit)