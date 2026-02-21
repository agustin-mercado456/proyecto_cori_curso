class TipoServicio:
    def __init__(self, id_tipo_servicio=None, nombre="", descripcion="", tarifa_base=0.0, activo=True):
        self.id_tipo_servicio = id_tipo_servicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.tarifa_base = tarifa_base
        self.activo = activo