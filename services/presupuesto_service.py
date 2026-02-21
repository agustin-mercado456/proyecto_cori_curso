import os
from datetime import datetime
from fpdf import FPDF
from repositories.config_repository import ConfigRepository
from repositories.presupuesto_repository import PresupuestoRepository

class PresupuestoService:
    def __init__(self):

        self.presupuesto_repo = PresupuestoRepository()

    def guardar_presupuesto(self, datos:dict):

        print('datos desde el servicio', datos)

        datos_repository = self.calcular_presupuesto(datos)

        # Capturamos la respuesta del repositorio
        exito, mensaje = self.presupuesto_repo.guardar_presupuesto_completo(datos_repository)
        
        # Si se guardó correctamente en la BD, generamos el PDF
        if exito:
            try:
                ruta_pdf = self.generar_pdf(datos_repository)
                # Le sumamos al mensaje original la ruta del PDF
                mensaje += f"\n\nAdemás, el PDF fue generado con éxito en:\n{ruta_pdf}"
            except Exception as e:
                mensaje += f"\n\n(Advertencia: Se guardó en BD, pero falló la creación del PDF: {e})"

        return exito, mensaje
        
        

    def calcular_presupuesto(self, datos:dict):

        if datos["servicio_nombre"] == "Medicion de Ruido" or datos["servicio_nombre"] == "Medicion de Iluminacion":
            if datos["requiere_croquis"] == True:
                datos["total"] = 2*(datos["kilometros"] * datos["precio_km"]) + datos["cantidad_puestos"] * datos["precio_puesto"] + datos["precio_croquis"] 
            else:
                datos["total"] = datos["kilometros"] * datos["precio_km"] + datos["cantidad_puestos"] * datos["precio_puesto"]       
        
        if datos["servicio_nombre"] == "RGRL":
            datos["total"] = datos["kilometros"] * datos["precio_km"] + datos["cantidad_horas"] * datos["precio_hora"]
        
        if datos["servicio_nombre"] == "Capacitacion":
            datos["total"] = datos["kilometros"] * datos["precio_km"] + datos["precio_capacitacion"]
            
        return datos
        
       
    def generar_pdf(self, datos:dict):
        # 1. Crear carpeta 'presupuestos_pdf' si no existe
        carpeta_destino = "presupuestos_pdf"
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)

        # 2. Inicializar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # --- ENCABEZADO ---
        pdf.set_font("helvetica", "B", 16)
        pdf.cell(0, 10, "PRESUPUESTO DE SERVICIO - HIGIENE Y SEGURIDAD", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        # --- DATOS GENERALES ---
        fecha_actual = datetime.now().strftime("%d/%m/%Y - %H:%M hs")
        pdf.set_font("helvetica", "", 12)
        
        pdf.cell(0, 8, f"Fecha de emision: {fecha_actual}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"ID de Cliente: {datos.get('id_cliente')}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, f"Servicio a realizar: {datos.get('servicio_nombre')}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

        # --- DETALLE DEL CÁLCULO ---
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 8, "Detalle del Presupuesto:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("helvetica", "", 11)

        pdf.cell(0, 6, f"- Distancia de viaje: {datos.get('kilometros')} km (Costo por Km: ${datos.get('precio_km'):.2f})", new_x="LMARGIN", new_y="NEXT")

        # Variables específicas según el texto exacto sin tildes de tu código
        servicio = datos.get("servicio_nombre")
        
        if servicio in ["Medicion de Ruido", "Medicion de Iluminacion"]:
            pdf.cell(0, 6, f"- Cantidad de puestos: {datos.get('cantidad_puestos')} (Costo por puesto: ${datos.get('precio_puesto'):.2f})", new_x="LMARGIN", new_y="NEXT")
            texto_croquis = "Si" if datos.get("requiere_croquis") else "No"
            pdf.cell(0, 6, f"- Requiere diseño de croquis: {texto_croquis}", new_x="LMARGIN", new_y="NEXT")
            if datos.get("requiere_croquis"):
                pdf.cell(0, 6, f"- Costo del croquis: ${datos.get('precio_croquis'):.2f}", new_x="LMARGIN", new_y="NEXT")

        elif servicio == "RGRL":
            pdf.cell(0, 6, f"- Horas estimadas: {datos.get('cantidad_horas')} hs (Costo por hora: ${datos.get('precio_hora'):.2f})", new_x="LMARGIN", new_y="NEXT")

        elif servicio == "Capacitacion":
            pdf.cell(0, 6, f"- Valor de la capacitacion: ${datos.get('precio_capacitacion'):.2f}", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(10)

        # --- TOTAL ---
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, f"TOTAL PRESUPUESTADO: ${datos.get('total'):,.2f}", border=1, align="C", new_x="LMARGIN", new_y="NEXT")

        # --- GUARDAR ARCHIVO ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"Presupuesto_Cliente{datos.get('id_cliente')}_{timestamp}.pdf"
        ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
        
        pdf.output(ruta_completa)
        
        return ruta_completa