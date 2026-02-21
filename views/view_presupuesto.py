import tkinter as tk
from tkinter import ttk, messagebox
from controllers.cliente_controller import ClienteController
from controllers.servicio_controller import ServicioController
from controllers.presupuesto_controller import PresupuestoController
from datetime import datetime

class PresupuestoForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Presupuestos Unificado")
        self.root.geometry("850x700") # Reduje un poco la altura al quitar elementos
        self.root.config(bg="white")
        
        # --- INSTANCIAS ---
        self.cliente_controller = ClienteController()
        self.servicio_controller = ServicioController()
        self.presupuesto_controller = PresupuestoController()
        
        # --- VARIABLES DE CLIENTE ---
        self.id_cliente_seleccionado = tk.IntVar(value=0)
        self.cuit_buscar_var = tk.StringVar()
        self.nombre_cliente_var = tk.StringVar(value="Ninguno seleccionado")

        # --- VARIABLES DE SERVICIO COMPARTIDAS ---
        self.servicio_seleccionado = tk.StringVar()
        self.id_servicio_seleccionado = tk.IntVar(value=0)
        self.mapa_servicios = {} 
        self.km_var = tk.DoubleVar(value=0.0)
        
        # --- Variables Mediciones ---
        self.puestos_var = tk.IntVar(value=0)
        self.precio_puesto_var = tk.DoubleVar(value=0.0)
        self.croquis_var = tk.BooleanVar(value=False)
        self.precio_croquis_var = tk.DoubleVar(value=0.0)
        
        # --- Variables RGRL ---
        self.horas_var = tk.IntVar(value=0)
        self.precio_hora_var = tk.DoubleVar(value=0.0)
        
        # --- Variables Capacitación ---
        self.precio_cap_var = tk.DoubleVar(value=0.0)

        self.dibujar_pantalla()

    def dibujar_pantalla(self):
        tk.Label(self.root, text="Generador de Presupuestos", 
                 bg="#2980b9", fg="white", font=("Arial", 16, "bold"), pady=10).pack(fill="x")

        # --- 1. SELECCIÓN DE CLIENTE ---
        frame_cliente = tk.LabelFrame(self.root, text=" 1. Selección de Cliente ", bg="white", font=("Arial", 10, "bold"), padx=15, pady=10)
        frame_cliente.pack(fill="x", padx=20, pady=5)
        
        tk.Label(frame_cliente, text="Buscar por CUIT:", bg="white").grid(row=0, column=0, pady=5, sticky="w")
        tk.Entry(frame_cliente, textvariable=self.cuit_buscar_var).grid(row=0, column=1, padx=10, pady=5)
        tk.Button(frame_cliente, text="BUSCAR", bg="#3498db", fg="white", relief="flat", cursor="hand2", 
                  command=self.buscar_cliente).grid(row=0, column=2, padx=10)
        
        tk.Label(frame_cliente, text="Cliente actual:", bg="white", font=("Arial", 9, "bold")).grid(row=1, column=0, pady=5, sticky="w")
        tk.Label(frame_cliente, textvariable=self.nombre_cliente_var, bg="white", fg="#27ae60", font=("Arial", 10, "bold")).grid(row=1, column=1, columnspan=2, sticky="w")

        # --- 2. SELECCIÓN DE SERVICIO ---
        frame_top = tk.Frame(self.root, bg="white", pady=5)
        frame_top.pack(fill="x", padx=20)
        
        tk.Label(frame_top, text="2. Seleccione el Tipo de Servicio:", bg="white", font=("Arial", 11, "bold")).pack(anchor="w")
        
        servicios_bd = self.servicio_controller.listar_servicios(solo_activos=True)
        
        nombres_servicios = []
        for s in servicios_bd:
            nombres_servicios.append(s.nombre)
            self.mapa_servicios[s.nombre] = s.id_tipo_servicio 
            
        combo = ttk.Combobox(frame_top, textvariable=self.servicio_seleccionado, values=nombres_servicios, state="readonly", width=40)
        combo.pack(anchor="w", pady=5)
        combo.bind("<<ComboboxSelected>>", self.actualizar_formulario)

        # --- 3. FRAME DINÁMICO (VARIABLES) ---
        self.frame_dinamico = tk.LabelFrame(self.root, text=" 3. Variables de Cálculo ", bg="white", font=("Arial", 10, "bold"), padx=15, pady=15)
        self.frame_dinamico.pack(fill="both", expand=True, padx=20, pady=5)

        # --- 4. FRAME RESULTADO Y GUARDADO ---
        frame_resultado = tk.Frame(self.root, bg="#ecf0f1", pady=10, bd=1, relief="solid")
        frame_resultado.pack(fill="x", padx=20, pady=10)
        
        # Botón único
        tk.Button(frame_resultado, text="GENERAR Y GUARDAR PRESUPUESTO", bg="#e67e22", fg="white", font=("Arial", 12, "bold"), 
                  cursor="hand2", command=self.enviar_a_guardar, pady=5).pack(pady=10)

    # ================= FUNCIONES =================

    def buscar_cliente(self):
        cuit = self.cuit_buscar_var.get()
        
        if not cuit or cuit.strip() == "":
            messagebox.showwarning("Atención", "Ingrese un CUIT para buscar.")
            return
            
        cliente = self.cliente_controller.buscar_cliente_por_cuit(cuit.strip())
        
        if cliente:
            self.id_cliente_seleccionado.set(cliente.id_cliente)
            self.nombre_cliente_var.set(f"{cliente.razon_social} (ID: {cliente.id_cliente})")
            messagebox.showinfo("Éxito", "Cliente encontrado y seleccionado.")
        else:
            self.id_cliente_seleccionado.set(0)
            self.nombre_cliente_var.set("Ninguno seleccionado")
            messagebox.showerror("Error", "No existe ningún cliente registrado con ese CUIT.")

    def actualizar_formulario(self, event=None):
        for widget in self.frame_dinamico.winfo_children():
            widget.destroy()
            
        servicio = self.servicio_seleccionado.get()

        # Usamos los nombres exactos tal cual están cargados en tu base de datos
        if servicio in ["Medicion de Ruido", "Medicion de Iluminacion"]:
            self._dibujar_inputs_mediciones()
        elif servicio == "RGRL":
            self._dibujar_inputs_rgrl()
        elif servicio == "Capacitacion":
            self._dibujar_inputs_capacitacion()
        else:
            # Por si selecciona "Asesoramiento Presencial" o "Carga de Matafuegos" que no definimos UI todavía
            tk.Label(self.frame_dinamico, text="No hay variables configuradas para este servicio.", bg="white", fg="red").pack(pady=20)

    def _dibujar_inputs_mediciones(self):
        tk.Label(self.frame_dinamico, text="Distancia total a recorrer (Km):", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.km_var).grid(row=0, column=1, pady=5, padx=10)

        tk.Label(self.frame_dinamico, text="Cantidad de puestos a medir:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.puestos_var).grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(self.frame_dinamico, text="Precio cobrado por puesto ($):", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.precio_puesto_var).grid(row=2, column=1, pady=5, padx=10)

        tk.Checkbutton(self.frame_dinamico, text="¿Requiere diseño de croquis? (Duplica costo de viaje)", 
                       variable=self.croquis_var, bg="white").grid(row=3, column=0, columnspan=2, sticky="w", pady=10)
        
        tk.Label(self.frame_dinamico, text="Costo adicional por hacer el croquis ($):", bg="white").grid(row=4, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.precio_croquis_var).grid(row=4, column=1, pady=5, padx=10)

    def _dibujar_inputs_rgrl(self):
        tk.Label(self.frame_dinamico, text="Distancia total a recorrer (Km):", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.km_var).grid(row=0, column=1, pady=5, padx=10)

        tk.Label(self.frame_dinamico, text="Horas estimadas de trabajo:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.horas_var).grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(self.frame_dinamico, text="Precio cobrado por hora ($):", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.precio_hora_var).grid(row=2, column=1, pady=5, padx=10)

    def _dibujar_inputs_capacitacion(self):
        tk.Label(self.frame_dinamico, text="Distancia total a recorrer (Km):", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.km_var).grid(row=0, column=1, pady=5, padx=10)

        tk.Label(self.frame_dinamico, text="Valor fijo de la capacitación ($):", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(self.frame_dinamico, textvariable=self.precio_cap_var).grid(row=1, column=1, pady=5, padx=10)

    def enviar_a_guardar(self):
        if self.id_cliente_seleccionado.get() == 0:
            messagebox.showwarning("Atención", "Debe buscar y seleccionar un cliente primero.")
            return
            
        servicio_nombre = self.servicio_seleccionado.get()
        if not servicio_nombre:
            messagebox.showwarning("Atención", "Debe seleccionar un tipo de servicio.")
            return

        try:
            id_servicio = self.mapa_servicios.get(servicio_nombre, 0)

            # 1. Armamos la BASE del diccionario con lo que todos los servicios comparten
            datos_presupuesto = {
                "id_cliente": self.id_cliente_seleccionado.get(),
                "id_tipo_servicio": id_servicio, 
                "servicio_nombre": servicio_nombre,
                "cantidad": 1,
                "kilometros": self.km_var.get(),
                "precio_km": 600.00,
            }

            # 2. Inyectamos solo las variables que corresponden al servicio elegido
            if servicio_nombre in ["Medicion de Ruido", "Medicion de Iluminacion"]:

                datos_presupuesto["cantidad_puestos"] = self.puestos_var.get()
                datos_presupuesto["precio_puesto"] = self.precio_puesto_var.get()
                datos_presupuesto["precio_croquis"] = self.precio_croquis_var.get()
                datos_presupuesto["requiere_croquis"] = self.croquis_var.get()

            elif servicio_nombre == "RGRL":
                datos_presupuesto["cantidad_horas"] = self.horas_var.get()
                datos_presupuesto["precio_hora"] = self.precio_hora_var.get()

            elif servicio_nombre == "Capacitacion":
                datos_presupuesto["precio_capacitacion"] = self.precio_cap_var.get()
                
            else:
                messagebox.showwarning("Atención", "Este servicio no tiene variables configuradas.")
                return

            # 3. Enviamos el diccionario a medida al controlador
            resultado = self.presupuesto_controller.guardar_presupuesto_completo(datos_presupuesto)
            
            if resultado[0]:
                messagebox.showinfo("Éxito", resultado[1])
            else:
                messagebox.showerror("Error", resultado[1])
                
        except tk.TclError:
             messagebox.showerror("Error", "Asegúrese de que todos los campos numéricos estén completos correctamente.")