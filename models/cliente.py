class Cliente:
    # Agregamos ="" al final de direccion
    def __init__(self, id_cliente=None, razon_social="", cuit_cuil="", rubro="", localidad="", provincia="", direccion=""):
        self.id_cliente = id_cliente
        self.razon_social = razon_social
        self.cuit_cuil = cuit_cuil
        self.rubro = rubro
        self.localidad = localidad
        self.provincia = provincia
        self.direccion = direccion